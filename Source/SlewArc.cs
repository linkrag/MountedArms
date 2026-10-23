using System;
using System.Reflection;
using HarmonyLib;
using RimWorld;
using UnityEngine;
using Verse;

namespace MountedArms
{
    /// <summary>
    /// Vanilla turrets only (Building_TurretGun). Combat Extended has its own systems for this
    /// (NonSnapTurretExtension and CompFireArc) and this comp stays inert there.
    /// - degreesPerSecond: the gun top slews toward its target instead of snapping; a burst only starts
    ///   once the barrel is within aimTolerance degrees of the target.
    /// - arcDegrees: total width of the fire arc centered on the building rotation (0 = 360 degrees).
    /// </summary>
    public class CompProperties_TurretSlew : CompProperties
    {
        public float degreesPerSecond = 40f;
        public float aimTolerance = 4f;
        public float arcDegrees = 0f;

        public CompProperties_TurretSlew()
        {
            compClass = typeof(CompTurretSlew);
        }
    }

    public class CompTurretSlew : ThingComp
    {
        private static readonly FieldInfo WarmupField = AccessTools.Field(typeof(Building_TurretGun), "burstWarmupTicksLeft");

        /// <summary>Degrees the barrel still has to turn to face the current target (set by the TurretTop patch).</summary>
        public float remaining;

        public CompProperties_TurretSlew Props => (CompProperties_TurretSlew)props;

        public bool IsVanillaGun => parent is Building_TurretGun;

        public bool WithinArc(LocalTargetInfo targ)
        {
            if (Props.arcDegrees <= 0f || Props.arcDegrees >= 359f || !targ.IsValid)
            {
                return true;
            }
            Vector3 d = targ.CenterVector3 - parent.DrawPos;
            d.y = 0f;
            if (d.sqrMagnitude < 0.01f)
            {
                return true;
            }
            return Mathf.Abs(Mathf.DeltaAngle(parent.Rotation.AsAngle, d.AngleFlat())) <= Props.arcDegrees / 2f;
        }

        public override void CompTick()
        {
            base.CompTick();
            if (!IsVanillaGun || !parent.Spawned || Props.degreesPerSecond <= 0f || WarmupField == null)
            {
                return;
            }
            // Hold the shot at the last warmup tick until the barrel is on target.
            if (remaining > Props.aimTolerance && (int)WarmupField.GetValue(parent) == 1)
            {
                WarmupField.SetValue(parent, 2);
            }
        }

        public override void PostDrawExtraSelectionOverlays()
        {
            base.PostDrawExtraSelectionOverlays();
            if (!IsVanillaGun || Props.arcDegrees <= 0f || Props.arcDegrees >= 359f)
            {
                return;
            }
            Building_Turret t = (Building_Turret)parent;
            float range = t.AttackVerb != null ? t.AttackVerb.verbProps.range : 20f;
            range = Mathf.Min(range, 30f);
            Vector3 c = parent.TrueCenter();
            c.y = AltitudeLayer.MetaOverlays.AltitudeFor();
            float half = Props.arcDegrees / 2f;
            float a = parent.Rotation.AsAngle;
            GenDraw.DrawLineBetween(c, c + Vector3.forward.RotatedBy(a - half) * range, SimpleColor.White);
            GenDraw.DrawLineBetween(c, c + Vector3.forward.RotatedBy(a + half) * range, SimpleColor.White);
        }
    }

    [HarmonyPatch(typeof(TurretTop), nameof(TurretTop.TurretTopTick))]
    public static class TurretTop_Slew_Patch
    {
        private static readonly FieldInfo ParentField = AccessTools.Field(typeof(TurretTop), "parentTurret");

        public static void Prefix(TurretTop __instance, out float __state)
        {
            __state = __instance.CurRotation;
        }

        public static void Postfix(TurretTop __instance, float __state)
        {
            try
            {
                Building_TurretGun turret = ParentField?.GetValue(__instance) as Building_TurretGun;
                CompTurretSlew comp = turret?.GetComp<CompTurretSlew>();
                if (comp == null || comp.Props.degreesPerSecond <= 0f)
                {
                    return;
                }
                if (turret.CurrentTarget.IsValid)
                {
                    float step = comp.Props.degreesPerSecond / 60f;
                    float delta = Mathf.DeltaAngle(__state, __instance.CurRotation);
                    float move = Mathf.Clamp(delta, -step, step);
                    __instance.CurRotation = __state + move;
                    comp.remaining = Mathf.Abs(delta - move);
                }
                else
                {
                    comp.remaining = 0f;
                }
            }
            catch (Exception e)
            {
                Log.ErrorOnce("[Mounted Arms] Slew patch error: " + e, 7281932);
            }
        }
    }

    [HarmonyPatch(typeof(Building_TurretGun), "IsValidTarget")]
    public static class TurretGun_IsValidTarget_ArcPatch
    {
        public static void Postfix(Building_TurretGun __instance, Thing t, ref bool __result)
        {
            if (!__result || t == null)
            {
                return;
            }
            CompTurretSlew comp = __instance.GetComp<CompTurretSlew>();
            if (comp != null && !comp.WithinArc(t))
            {
                __result = false;
            }
        }
    }

    [HarmonyPatch(typeof(Building_TurretGun), nameof(Building_TurretGun.OrderAttack))]
    public static class TurretGun_OrderAttack_ArcPatch
    {
        public static bool Prefix(Building_TurretGun __instance, LocalTargetInfo targ)
        {
            CompTurretSlew comp = __instance.GetComp<CompTurretSlew>();
            if (comp != null && !comp.WithinArc(targ))
            {
                Messages.Message("MA_OutOfArc".Translate(), __instance, MessageTypeDefOf.RejectInput, false);
                return false;
            }
            return true;
        }
    }
}
