using System.Collections.Generic;
using CombatExtended;
using HarmonyLib;
using RimWorld;
using UnityEngine;
using Verse;

namespace MountedArms.CE
{
    // CE-only assembly (Bin/<version>/CE/Assemblies, loaded only with Combat Extended). The main MountedArms.dll
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
            Vector3 origin3 = new Vector3(origin.x, 0f, origin.y);
            Vector3 dir3 = new Vector3(dir.x, 0f, dir.y);
            if (ext.ignitionDistance <= 0f || dir3.sqrMagnitude < 0.0001f)
            {
                LaunchFx.Play(map, origin3, dir3, ext);
                return;
            }
            // Steep shots (CIWS at shells/drop pods): the flight motor lights ignitionDistance along the 3D path,
            // which is fewer cells out horizontally but higher, and CE draws height as +0.84*height on z.
            // (Review finding: the flash used to land on the ground 4 cells out.)
            LaunchFxExtension puffsOnly = new LaunchFxExtension();
            puffsOnly.ejectPuffs = ext.ejectPuffs;
            puffsOnly.puffSize = ext.puffSize;
            puffsOnly.backblastPuffs = ext.backblastPuffs;
            puffsOnly.ignitionDistance = 0f;
            puffsOnly.flashSize = 0f;
            LaunchFx.Play(map, origin3, dir3, puffsOnly);
            float horizontal = ext.ignitionDistance * Mathf.Cos(__instance.shotAngle);
            float height = __instance.shotHeight + ext.ignitionDistance * Mathf.Sin(__instance.shotAngle);
            Vector3 ignition = origin3 + dir3.normalized * horizontal + new Vector3(0f, 0f, 0.84f * Mathf.Max(0f, height));
            LaunchFx.PlayIgnition(map, ignition, ext);
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
