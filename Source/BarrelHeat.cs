using System;
using System.Reflection;
using HarmonyLib;
using RimWorld;
using UnityEngine;
using Verse;

namespace MountedArms
{
    /// <summary>
    /// Barrel heat for any Building_Turret (vanilla Building_TurretGun and CE Building_TurretGunCE).
    /// Heat is 0..1. Each shot adds heatPerShot, the barrel cools coolPerSecond all the time.
    /// At 1.0 the turret is locked (cannot start new bursts) until it cools down to resumeAt.
    /// Only public API + reflection on the shared field "burstCooldownTicksLeft", so it needs no CE reference.
    /// </summary>
    public class CompProperties_BarrelHeat : CompProperties
    {
        /// <summary>Heat added per projectile fired (1.0 = overheated).</summary>
        public float heatPerShot = 0.03f;
        /// <summary>Passive cooling per second.</summary>
        public float coolPerSecond = 0.02f;
        /// <summary>After overheating the turret fires again once heat drops to this value.</summary>
        public float resumeAt = 0.5f;
        /// <summary>Visible smoke above this heat.</summary>
        public float smokeAt = 0.7f;
        /// <summary>Vanilla only: extra aim error (cells at 20 cells distance) at full heat.</summary>
        public float heatSpread = 0f;
        /// <summary>Vanilla only: extra aim error (cells at 20 cells distance) added per shot already fired in the current burst.</summary>
        public float burstSpread = 0f;

        public CompProperties_BarrelHeat()
        {
            compClass = typeof(CompBarrelHeat);
        }
    }

    public class CompBarrelHeat : ThingComp
    {
        private static readonly FieldInfo BurstShotsLeft = AccessTools.Field(typeof(Verb), "burstShotsLeft");

        private float heat;
        private bool overheated;
        private int prevBurstLeft;
        private int burstShots;

        private FieldInfo cooldownField;
        private MethodInfo resetTargetMethod;
        private bool reflected;

        public CompProperties_BarrelHeat Props => (CompProperties_BarrelHeat)props;

        public float Heat => heat;
        public bool Overheated => overheated;

        /// <summary>Aim error radius in cells at 20 cells distance (vanilla projectile patch).</summary>
        public float CurrentSpread()
        {
            return heat * Props.heatSpread + burstShots * Props.burstSpread;
        }

        private void Reflect()
        {
            reflected = true;
            Type t = parent.GetType();
            cooldownField = AccessTools.Field(t, "burstCooldownTicksLeft");
            resetTargetMethod = AccessTools.Method(t, "ResetCurrentTarget");
            if (cooldownField == null || resetTargetMethod == null)
            {
                Log.ErrorOnce("[Mounted Arms] Barrel heat could not hook " + t.FullName + "; heat lock disabled.", 7281931);
            }
        }

        public override void CompTick()
        {
            base.CompTick();
            Building_Turret turret = parent as Building_Turret;
            if (turret == null || !parent.Spawned)
            {
                return;
            }
            if (!reflected)
            {
                Reflect();
            }

            // 1. Count shots fired this tick from the verb's burst counter.
            Verb verb = turret.AttackVerb;
            if (verb != null && BurstShotsLeft != null)
            {
                int cur = (int)BurstShotsLeft.GetValue(verb);
                int shots = 0;
                if (verb.state == VerbState.Bursting)
                {
                    if (cur < prevBurstLeft) shots = prevBurstLeft - cur;
                    else if (cur > prevBurstLeft) shots = 1; // burst just started: the first shot was already fired
                    prevBurstLeft = cur;
                }
                else
                {
                    if (prevBurstLeft > 0) shots = 1; // last shot of the burst
                    prevBurstLeft = 0;
                }
                if (shots > 0)
                {
                    heat += shots * Props.heatPerShot;
                    burstShots += shots;
                }
                if (verb.state != VerbState.Bursting && shots == 0)
                {
                    burstShots = 0;
                }
            }

            // 2. Cooling.
            heat -= Props.coolPerSecond / 60f;
            heat = Mathf.Clamp01(heat);

            // 3. Overheat state.
            if (!overheated && heat >= 0.999f)
            {
                overheated = true;
                if (parent.Faction == Faction.OfPlayer)
                {
                    Messages.Message("MA_BarrelOverheated".Translate(parent.LabelCap), parent, MessageTypeDefOf.NegativeEvent, false);
                }
            }
            else if (overheated && heat <= Props.resumeAt)
            {
                overheated = false;
            }

            if (overheated && cooldownField != null)
            {
                int cd = (int)cooldownField.GetValue(parent);
                if (cd < 3)
                {
                    cooldownField.SetValue(parent, 3);
                }
                if (turret.CurrentTarget.IsValid && (verb == null || verb.state != VerbState.Bursting))
                {
                    resetTargetMethod?.Invoke(parent, null);
                }
            }

            // 4. Smoke when hot.
            if (heat >= Props.smokeAt && parent.IsHashIntervalTick(overheated ? 12 : 30))
            {
                FleckMaker.ThrowSmoke(parent.DrawPos, parent.Map, overheated ? 1.4f : 0.8f);
            }
        }

        public override string CompInspectStringExtra()
        {
            string s = "MA_BarrelHeat".Translate() + ": " + heat.ToStringPercent("F0");
            if (overheated)
            {
                s += " (" + "MA_BarrelCooling".Translate() + ")";
            }
            return s;
        }

        public override void PostExposeData()
        {
            base.PostExposeData();
            Scribe_Values.Look(ref heat, "mountedArmsHeat", 0f);
            Scribe_Values.Look(ref overheated, "mountedArmsOverheated", false);
        }
    }
}
