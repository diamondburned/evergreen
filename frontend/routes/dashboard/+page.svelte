<script lang="ts">
  import LoadingDots from "$lib/components/LoadingDots.svelte";
  import WhitePage from "$lib/components/WhitePage.svelte";
  import Roadmap from "$lib/components/roadmap/Roadmap.svelte";

  import categories_ from "$lib/categories.json";
  import { type Categories } from "$lib/components/roadmap/Roadmap.svelte";

  import { listScores, type ScoreSubmission } from "$lib/api";
  import { onMount } from "svelte";

  import { Chart, HistogramSeries, LineSeries } from "svelte-lightweight-charts";
  import { ColorType, type DeepPartial, type TimeChartOptions } from "lightweight-charts";

  $: categories = categories_ as unknown as Categories; // fix typescript error

  const styles = window.getComputedStyle(document.body);
  const mutedColor = styles.getPropertyValue("--primary-rgb");

  const chartOpts: DeepPartial<TimeChartOptions> = {
    height: 350,
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
      scaleMargins: { top: 0.05, bottom: 0.05 },
    },
    timeScale: {
      lockVisibleTimeRangeOnResize: true,
      borderVisible: false,
      timeVisible: true,
      secondsVisible: false,
      fixLeftEdge: true,
      fixRightEdge: true,
    },
  };

  function formatSeconds(seconds: number, long = false) {
    const m = Math.floor(seconds / 60);
    const s = Math.ceil(seconds % 60);
    if (long) {
      if (m == 0) {
        return s == 1 ? `${s} second` : `${s} seconds`;
      }
      const mm = m == 1 ? `${m} minute` : `${m} minutes`;
      const ss = s == 1 ? `${s} second` : `${s} seconds`;
      return `${mm} and ${ss}`;
    }
    return `${m}:${s < 10 ? "0" : ""}${s}`;
  }

  function subtractDays(date: Date, days: number) {
    const result = new Date(date);
    result.setDate(result.getDate() - days);
    result.setHours(0, 0, 0, 0);
    return result;
  }

  function startOfDay(date: Date) {
    const result = new Date(date);
    result.setHours(0, 0, 0, 0);
    return result;
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
  $: timeRange = [subtractDays(now, 7), now];

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
          date.setDate(date.getDate() - i);
          date.setHours(0, 0, 0, 0);
          return {
            date,
            scores: scores.filter((score) => {
              const scoreDate = new Date(Date.parse(score.submitted_at! + "Z"));
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
    console.log(dailyScores);
    return [
      {
        time: Math.round(timeRange[0].getTime() / 1000),
        value: 0,
      },
      ...dailyScores.map((day) => ({
        time: Math.round(day.date.getTime() / 1000) - day.date.getTimezoneOffset() * 60,
        value: valueFn(day.scores),
      })),
    ];
  }

  $: dailyScoresData = mapPastWeekScores(pastWeekScores, (dayScores) => dayScores.length);
  $: averageTimesData = mapPastWeekScores(pastWeekScores, (dayScores) => {
    return dayScores.length === 0
      ? 0
      : dayScores.reduce((sum, score) => sum + score.time_taken, 0) / dayScores.length;
  });

  let currentStreak = "";
  $: {
    const lost = dailyScoresData
      ? dailyScoresData
          .slice()
          .reverse()
          .findIndex((day) => day.value === 0)
      : 0;
    currentStreak = lost == -1 ? `${dailyScoresData!.length}+` : `${lost}`;
    currentStreak = lost == 1 ? `${currentStreak} day` : `${currentStreak} days`;
  }

  let currentAverageTimes = "";
  $: {
    const data = (averageTimesData || []).filter((day) => day.value > 0);
    const avg = data ? data.reduce((sum, day) => sum + day.value, 0) / data.length : 0;
    currentAverageTimes = formatSeconds(avg, true);
  }
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

          <p>Current Streak: <span class="value">{currentStreak}</span></p>
          <Chart {...chartOpts}>
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

          <p>Current Average: <span class="value">{currentAverageTimes}</span></p>
          <Chart {...chartOpts}>
            <LineSeries
              data={averageTimesData}
              priceFormat={{
                type: "custom",
                formatter: formatSeconds,
              }}
            />
          </Chart>
        </article>
      </div>
    {/if}
  </section>
</WhitePage>

<style lang="scss">
  h2 {
    font-size: 1.75em;
  }

  section {
    display: flex;
    flex-direction: column;
    margin: 1rem auto;
    width: 100%;
  }

  section:last-child {
    margin-bottom: 4rem;
  }

  section.container {
    align-items: baseline;
  }

  .stats-cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    grid-gap: 1.5rem;
    width: 100%;

    article {
      padding: 1rem;
      border: 1px solid var(--primary);
      border-radius: 15px;
      transition: all 0.15s ease-in-out;

      &:hover {
        box-shadow: 0 12px 12px 0 rgba(0, 0, 0, 0.1);
        transform: scale(1.025);
      }

      h3 {
        margin: 0.5rem 0;
      }

      hgroup p {
        margin-top: 0;
        font-size: 0.9rem;
      }

      span.value {
        font-weight: bold;
      }
    }
  }

  .roadmap-section {
    /* max-width: 1200px; */
    margin-left: auto;
    margin-right: auto;
    position: relative;

    h2 {
      position: absolute;
      margin: 0;
    }
  }
</style>
