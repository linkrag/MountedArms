using RimWorld;
using UnityEngine;
using Verse;

namespace MountedArms
{
    /// <summary>
    /// Rocket exhaust at the nozzle, for projectiles (vanilla or CE). Replaces CE's CompProperties_ProjectileFleck,
    /// which places the flame at DrawPos minus the last tick's movement x originOffset (speed-dependent, so it sat
    /// mid-missile). Here it sits nozzleDistance cells behind the drawn position, along the drawn heading.
    /// Same component as Mounted Arms: Strategic's (the mods do not depend on each other).
    /// </summary>
    public class CompProperties_Exhaust : CompProperties
    {
        public FleckDef flameFleck;
        public FleckDef smokeFleck;
        public float nozzleDistance = 1f;
        public float flameScale = 1f;
        public int flamePerTick = 2;
        public float smokeScale = 1.5f;
        public float smokeChance = 0.6f;
        public int flameTicks = -1;

        public CompProperties_Exhaust()
        {
            compClass = typeof(CompExhaust);
        }
    }

    public class CompExhaust : ThingComp
    {
        private Vector3 lastPos;
        private Vector3 heading;
        private int age;

        public CompProperties_Exhaust Props
        {
            get { return (CompProperties_Exhaust)props; }
        }

        public override void CompTick()
        {
            base.CompTick();
            Map map = parent.Map;
            if (!parent.Spawned || map == null)
            {
                return;
            }
            Vector3 pos = parent.DrawPos;
            age++;
            Vector3 delta = pos - lastPos;
            delta.y = 0f;
            if (age > 1 && delta.sqrMagnitude > 0.000001f)
            {
                heading = delta.normalized;
            }
            lastPos = pos;
            if (heading == Vector3.zero)
            {
                return;
            }
            Vector3 nozzle = pos - heading * Props.nozzleDistance;
            float angle = heading.AngleFlat();
            if (Props.flameFleck != null && (Props.flameTicks < 0 || age <= Props.flameTicks))
            {
                for (int i = 0; i < Props.flamePerTick; i++)
                {
                    FleckCreationData flame = FleckMaker.GetDataStatic(nozzle - heading * Rand.Range(0f, 0.25f), map, Props.flameFleck, Props.flameScale * Rand.Range(0.8f, 1.2f));
                    flame.rotation = angle;
                    map.flecks.CreateFleck(flame);
                }
            }
            if (Props.smokeFleck != null && Rand.Chance(Props.smokeChance))
            {
                FleckCreationData smoke = FleckMaker.GetDataStatic(nozzle - heading * 0.3f, map, Props.smokeFleck, Props.smokeScale * Rand.Range(0.8f, 1.2f));
                smoke.rotation = Rand.Range(0f, 360f);
                map.flecks.CreateFleck(smoke);
            }
        }
    }
}
