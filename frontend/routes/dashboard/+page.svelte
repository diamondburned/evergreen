<script lang="ts">
  import WhitePage from "$lib/components/WhitePage.svelte";
  import Roadmap from "$lib/components/roadmap/Roadmap.svelte";
  import categories_ from "$lib/categories.json";
  import { type Categories } from "$lib/components/roadmap/Roadmap.svelte";
  import { listScores, type ScoreSubmission } from "$lib/api";
  import { onMount } from "svelte";
  import { Chart, TimeScale, HistogramSeries } from "svelte-lightweight-charts";
  import { ColorType, type DeepPartial, type TimeChartOptions } from "lightweight-charts";
  import LoadingDots from "$lib/components/LoadingDots.svelte";

  $: categories = categories_ as unknown as Categories; // fix typescript error

  const styles = window.getComputedStyle(document.body);
  const mutedColor = styles.getPropertyValue("--primary-rgb");

  const chartOpts: DeepPartial<TimeChartOptions> = {
    width: 800,
    height: 400,
    autoSize: true,
    handleScale: false,
    handleScroll: false,
    grid: {
      vertLines: { visible: false },
      horzLines: { visible: true, color: `rgba(${mutedColor}, 0.25)` },
    },
    layout: {
      background: { type: ColorType.Solid, color: "transparent" },
      textColor: styles.color,
      fontFamily: styles.fontFamily,
    },
    rightPriceScale: {
      borderVisible: false,
      scaleMargins: { top: 0.05, bottom: 0 },
    },
  };

  function startOfWeek(date: Date) {
    const diff = date.getDate() - date.getDay();
    return new Date(date.setDate(diff));
  }

  function endOfWeek(date: Date) {
    const diff = date.getDate() - date.getDay() + 6;
    return new Date(date.setDate(diff));
  }

  type DailySubmissions = {
    date: Date;
    scores: ScoreSubmission[];
  };

  let error: string | undefined;
  let scores: ScoreSubmission[] = [];
  let pastWeekScores: DailySubmissions[] = []; // today last
  let loading = true;

  let now = new Date();
  let timeRange: [Date, Date];
  $: timeRange = [startOfWeek(now), endOfWeek(now)];

  async function refresh() {
    error = undefined;
    loading = true;

    try {
      scores = await listScores({
        fromTime: timeRange[0].toISOString(),
        toTime: timeRange[1].toISOString(),
      });

      pastWeekScores = new Array(7)
        .fill([])
        .map((_, i) => {
          const date = new Date(now);
          date.setDate(date.getDate() - i + 1);
          return {
            date,
            scores: scores.filter((score) => {
              const scoreDate = new Date(Date.parse(score.submitted_at!));
              return (
                scoreDate.getDate() === date.getDate() &&
                scoreDate.getMonth() === date.getMonth() &&
                scoreDate.getFullYear() === date.getFullYear()
              );
            }),
          };
        })
        .reverse();
    } catch (err) {
      error = `${err}`;
      console.log(err);
    } finally {
      loading = false;
    }
  }
  onMount(() => refresh());

  function mapPastWeekScores(
    dailyScores: DailySubmissions[],
    valueFn: (_: ScoreSubmission[]) => number,
  ) {
    if (dailyScores.length === 0) {
      return null;
    }
    return [
      {
        time: Math.round(timeRange[0].getTime() / 1000),
        value: 0,
      },
      ...dailyScores.map((day) => ({
        time: Math.round(day.date.getTime() / 1000),
        value: valueFn(day.scores),
      })),
    ];
  }

  $: dailyScoresData = mapPastWeekScores(pastWeekScores, (dayScores) => dayScores.length);
</script>

<svelte:head>
  <title>Dashboard</title>
</svelte:head>

<WhitePage>
  <section class="container roadmap-section">
    <h2>Study Plan</h2>
    <Roadmap {categories} />
  </section>

  <section class="container">
    <h2>Dashboard</h2>

    {#if loading}
      <LoadingDots padded />
    {:else}
      <div class="stats-cards">
        <article>
          <hgroup>
            <h3>Streaks</h3>
            <p>Measure of how many days in a row you have completed your daily goal.</p>
          </hgroup>

          <p>Current Streak: 0</p>

          <Chart {...chartOpts}>
            <TimeScale
              lockVisibleTimeRangeOnResize={true}
              borderVisible={false}
              timeVisible={true}
              secondsVisible={false}
              fixLeftEdge={true}
              fixRightEdge={true}
            />
            <HistogramSeries
              data={dailyScoresData}
              priceFormat={{ type: "price", precision: 0, minMove: 1 }}
            />
          </Chart>
        </article>

        <article>
          <hgroup>
            <h3>Average Times</h3>
            <p>Measure of how long on average you took to solve a problem over time.</p>
          </hgroup>

          <p>Daily Average: 0</p>
        </article>
      </div>
    {/if}
  </section>
</WhitePage>

<style lang="scss">
  section {
    display: flex;
    flex-direction: column;
    margin: 1rem auto;
    width: 100%;
  }

  section:last-child {
    margin-bottom: 2rem;
  }

  section.container {
    align-items: baseline;
  }

  .stats-cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
    grid-gap: 1rem;
    width: 100%;

    article {
      padding: 1rem;
      border: 1px solid var(--primary);
      border-radius: 15px;

      h3 {
        margin: 0.5rem 0;
      }

      hgroup p {
        margin-top: 0;
        font-size: 0.9rem;
      }
    }
  }

  .roadmap-section {
    /* max-width: 1200px; */
    margin-left: auto;
    margin-right: auto;
    position: relative;
  }
</style>
