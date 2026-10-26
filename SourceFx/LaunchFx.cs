using System;
using System.Reflection;
using HarmonyLib;
using RimWorld;
using UnityEngine;
using Verse;

namespace MountedArms
{
    // Separate assembly (Bin/<version>/Assemblies/MountedArmsFx.dll, loaded with and without CE), kept apart from
    // MountedArms.dll for historical reasons (it was C# 5 when only the .NET Framework csc existed). No CE
    // references here; the CE hook lives in MountedArmsCE.dll and reuses LaunchFx.Play.

    /// <summary>
    /// Launch effects for missile/rocket guns (on the GUN def, i.e. the turret's turretGunDef). Visual only:
    /// projectile speed and aim are untouched (CE's interception maths need linear flight).
    /// Soft launch (Stinger, TOW): a small eject puff and backblast at the tube, then the flight motor lights
    /// ignitionDistance cells away. Hot launch (rocket pods): ignitionDistance 0, flash at the muzzle.
    /// </summary>
    public class LaunchFxExtension : DefModExtension
    {
        public int ejectPuffs = 1;
        public float puffSize = 0.8f;
        public int backblastPuffs = 0;
        public float ignitionDistance = 0f;
        public float flashSize = 1.2f;
    }

    public static class LaunchFx
    {
        public static void Play(Map map, Vector3 origin, Vector3 direction, LaunchFxExtension ext)
        {
            if (map == null || ext == null)
            {
                return;
            }
            Vector3 dir = direction;
            dir.y = 0f;
            if (dir.sqrMagnitude < 0.0001f)
            {
                return;
            }
            dir.Normalize();
            origin.y = 0f;
            for (int i = 0; i < ext.ejectPuffs; i++)
            {
                FleckMaker.ThrowSmoke(origin + dir * 0.3f + Jitter(0.2f), map, ext.puffSize * Rand.Range(0.8f, 1.2f));
            }
            for (int i = 0; i < ext.backblastPuffs; i++)
            {
                FleckMaker.ThrowSmoke(origin - dir * Rand.Range(0.8f, 2f) + Jitter(0.4f), map, ext.puffSize * Rand.Range(1f, 1.4f));
            }
            PlayIgnition(map, origin + dir * ext.ignitionDistance, ext);
        }

        /// <summary>Ignition flash/sparks/smoke at a given point (the CE hook passes the drawn 3D position).</summary>
        public static void PlayIgnition(Map map, Vector3 ignition, LaunchFxExtension ext)
        {
            ignition.y = 0f;
            if (map == null || ext.flashSize <= 0f || !ignition.ToIntVec3().InBounds(map))
            {
                return;
            }
            FleckMaker.ThrowFireGlow(ignition, map, ext.flashSize);
            FleckMaker.ThrowMicroSparks(ignition, map);
            if (ext.ignitionDistance > 0f)
            {
                FleckMaker.ThrowSmoke(ignition, map, ext.flashSize * 0.7f);
            }
        }

        private static Vector3 Jitter(float r)
        {
            return new Vector3(Rand.Range(-r, r), 0f, Rand.Range(-r, r));
        }
    }

    [StaticConstructorOnStartup]
    public static class LaunchFxBootstrap
    {
        static LaunchFxBootstrap()
        {
            try
            {
                new Harmony("linkrag.mountedarms.fx").PatchAll(Assembly.GetExecutingAssembly());
            }
            catch (Exception e)
            {
                Log.Error("[Mounted Arms] Launch FX patching failed: " + e);
            }
        }
    }

    /// <summary>Vanilla projectiles: launch effects for turrets whose gun has LaunchFxExtension.</summary>
    [HarmonyPatch(typeof(Projectile), "Launch", new Type[]
    {
        typeof(Thing), typeof(Vector3), typeof(LocalTargetInfo), typeof(LocalTargetInfo),
        typeof(ProjectileHitFlags), typeof(bool), typeof(Thing), typeof(ThingDef)
    })]
    public static class Patch_VanillaLaunchFx
    {
        // origin already moved to the muzzle by MountedArms' prefix (Projectile_Launch_MuzzlePatch)
        public static void Postfix(Thing launcher, Vector3 origin, LocalTargetInfo usedTarget, Thing equipment)
        {
            try
            {
                Building_TurretGun turret = launcher as Building_TurretGun;
                if (turret == null)
                {
                    turret = equipment as Building_TurretGun;
                }
                if (turret == null || turret.def.building == null || turret.def.building.turretGunDef == null)
                {
                    return;
                }
                LaunchFxExtension ext = turret.def.building.turretGunDef.GetModExtension<LaunchFxExtension>();
                if (ext != null)
                {
                    LaunchFx.Play(turret.Map, origin, usedTarget.CenterVector3 - origin, ext);
                }
            }
            catch (Exception e)
            {
                Log.ErrorOnce("[Mounted Arms] Launch FX error: " + e, 7281931);
            }
        }
    }
}
