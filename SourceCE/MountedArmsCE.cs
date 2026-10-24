using System.Collections.Generic;
using CombatExtended;
using HarmonyLib;
using RimWorld;
using UnityEngine;
using Verse;

namespace MountedArms.CE
{
    // CE-only assembly (1.6/CE/Assemblies, loaded only with Combat Extended). The main MountedArms.dll
    // must not reference CE, so anything that needs CE types lives here.

    [StaticConstructorOnStartup]
    public static class MountedArmsCEInit
    {
        static MountedArmsCEInit()
        {
            new Harmony("linkrag.mountedarms.ce").PatchAll();
        }
    }

    /// <summary>
    /// CE projectiles: launch effects for guns with MountedArms.LaunchFxExtension (MountedArmsFx.dll).
    /// Every ProjectileCE launch (direct fire, artillery, world shots, CIWS interceptors) ends in this overload,
    /// with the gun as equipment. Visual only: speed and aim are untouched.
    /// </summary>
    [HarmonyPatch(typeof(ProjectileCE), "Launch", new System.Type[] { typeof(Thing), typeof(Vector2), typeof(Thing) })]
    public static class Patch_ProjectileCE_LaunchFx
    {
        public static void Postfix(ProjectileCE __instance, Vector2 origin, Thing equipment)
        {
            if (equipment == null)
            {
                return;
            }
            LaunchFxExtension ext = equipment.def.GetModExtension<LaunchFxExtension>();
            if (ext == null)
            {
                return;
            }
            Map map = __instance.Map ?? equipment.MapHeld;
            Vector2 dir = __instance.Destination - origin;
            LaunchFx.Play(map, new Vector3(origin.x, 0f, origin.y), new Vector3(dir.x, 0f, dir.y), ext);
        }
    }

    /// <summary>
    /// Adds an "Unload" button to Mounted Arms turrets. CE only offers unloading in the reload menu of
    /// a manned turret while it is manned; auto turrets need it too, to empty or swap ammo types.
    /// Building_CIWS_CE / Building_Turret_MultiVerbs call base.GetGizmos, so patching the base covers them.
    /// </summary>
    [HarmonyPatch(typeof(Building_TurretGunCE), "GetGizmos")]
    public static class Patch_TurretGizmos_Unload
    {
        public static IEnumerable<Gizmo> Postfix(IEnumerable<Gizmo> __result, Building_TurretGunCE __instance)
        {
            foreach (Gizmo g in __result)
            {
                yield return g;
            }
            if (!__instance.def.defName.StartsWith("MA_"))
            {
                yield break;
            }
            CompAmmoUser ammo = __instance.CompAmmo;
            if (ammo == null || !ammo.UseAmmo || !ammo.HasMagazine || __instance.Faction != Faction.OfPlayer)
            {
                yield break;
            }
            Command_Action cmd = new Command_Action();
            cmd.defaultLabel = "CE_UnloadLabel".Translate();
            cmd.defaultDesc = "MA_UnloadDesc".Translate();
            cmd.icon = ContentFinder<Texture2D>.Get("UI/Buttons/Reload", true);
            cmd.action = delegate { ammo.TryUnload(true); };
            if (ammo.CurMagCount <= 0)
            {
                cmd.Disable("MA_UnloadEmpty".Translate());
            }
            yield return cmd;
        }
    }
}
