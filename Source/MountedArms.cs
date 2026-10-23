using System;
using System.Collections.Generic;
using System.Reflection;
using HarmonyLib;
using RimWorld;
using UnityEngine;
using Verse;

namespace MountedArms
{
    /// <summary>
    /// Added to a turret ThingDef (modExtensions). Moves the projectile origin and muzzle flash
    /// from the turret center to the muzzle of the gun, along the line to the target.
    /// </summary>
    public class MuzzleExtension : DefModExtension
    {
        /// <summary>Distance in cells from the turret center (pivot of the gun sprite) to the muzzle.</summary>
        public float distance = 0.6f;

        /// <summary>Scale of the muzzle flash spawned at the muzzle. 0 = no flash.
        /// Set muzzleFlashScale to 0 on the gun verb so the vanilla flash (at the center) is not duplicated.</summary>
        public float flashScale = 9f;
    }

    /// <summary>Hides Combat Extended's "attack a world tile" artillery gizmo on this building.</summary>
    public class NoWorldStrikeExtension : DefModExtension { }

    public static class CeGizmoFilter
    {
        public static IEnumerable<Gizmo> Postfix(IEnumerable<Gizmo> __result, Thing __instance)
        {
            bool hide = __instance != null && __instance.def.GetModExtension<NoWorldStrikeExtension>() != null;
            foreach (Gizmo g in __result)
            {
                if (hide && g != null && g.GetType().Name == "Command_ArtilleryTarget") continue;
                yield return g;
            }
        }
    }

    [StaticConstructorOnStartup]
    public static class Bootstrap
    {
        static Bootstrap()
        {
            try
            {
                Harmony h = new Harmony("linkrag.mountedarms");
                h.PatchAll(Assembly.GetExecutingAssembly());
                Type ce = AccessTools.TypeByName("CombatExtended.Building_TurretGunCE");
                MethodInfo gg = ce == null ? null : AccessTools.DeclaredMethod(ce, "GetGizmos");
                if (gg != null)
                    h.Patch(gg, postfix: new HarmonyMethod(typeof(CeGizmoFilter), nameof(CeGizmoFilter.Postfix)));
            }
            catch (Exception e)
            {
                Log.Error("[Mounted Arms] Harmony patching failed: " + e);
            }
        }
    }

    [HarmonyPatch(typeof(Projectile), nameof(Projectile.Launch),
        new Type[]
        {
            typeof(Thing), typeof(Vector3), typeof(LocalTargetInfo), typeof(LocalTargetInfo),
            typeof(ProjectileHitFlags), typeof(bool), typeof(Thing), typeof(ThingDef)
        })]
    public static class Projectile_Launch_MuzzlePatch
    {
        public static void Prefix(Thing launcher, ref Vector3 origin, ref LocalTargetInfo usedTarget, Thing equipment)
        {
            try
            {
                // Automatic turret: launcher is the turret. Manned turret: launcher is the operator
                // pawn and the turret is passed as the equipment.
                Building_TurretGun turret = launcher as Building_TurretGun ?? equipment as Building_TurretGun;
                if (turret == null)
                {
                    return;
                }

                MuzzleExtension ext = turret.def.GetModExtension<MuzzleExtension>();
                if (ext == null)
                {
                    return;
                }

                Vector3 dir = usedTarget.CenterVector3 - origin;
                dir.y = 0f;
                if (dir.sqrMagnitude < 0.01f)
                {
                    return;
                }
                dir.Normalize();

                // Aim error from a hot barrel and from sustained bursts (vanilla projectiles only).
                CompBarrelHeat heat = turret.GetComp<CompBarrelHeat>();
                if (heat != null && turret.Map != null)
                {
                    float spread = heat.CurrentSpread();
                    if (spread > 0.05f)
                    {
                        float dist = (usedTarget.CenterVector3 - origin).magnitude;
                        spread *= Mathf.Clamp(dist / 20f, 0.3f, 2f);
                        Vector2 off = Rand.InsideUnitCircle * spread;
                        IntVec3 cell = usedTarget.Cell + new IntVec3(Mathf.RoundToInt(off.x), 0, Mathf.RoundToInt(off.y));
                        if (cell != usedTarget.Cell && cell.InBounds(turret.Map))
                        {
                            usedTarget = new LocalTargetInfo(cell);
                        }
                    }
                }

                origin += dir * ext.distance;

                if (ext.flashScale > 0.01f && turret.Map != null)
                {
                    FleckMaker.Static(origin, turret.Map, FleckDefOf.ShotFlash, ext.flashScale);
                }
            }
            catch (Exception e)
            {
                Log.ErrorOnce("[Mounted Arms] Muzzle patch error: " + e, 7281930);
            }
        }
    }
}
