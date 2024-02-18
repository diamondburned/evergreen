<script lang="ts">
  import WhitePage from "$lib/components/WhitePage.svelte";
  import Roadmap from "$lib/components/roadmap/Roadmap.svelte";
  import categories_ from "$lib/categories.json";
  import { type Categories } from "$lib/components/roadmap/Roadmap.svelte";
  import { listScores, type ScoreSubmission } from "$lib/api";
  import { onMount } from "svelte";

  import FusionCharts from 'fusioncharts';
  import Charts from 'fusioncharts/fusioncharts.charts';
  import FusionTheme from 'fusioncharts/themes/fusioncharts.theme.fusion';
  import SvelteFC, { fcRoot } from 'svelte-fusioncharts';

  fcRoot(FusionCharts, Charts, FusionTheme);

  $: categories = categories_ as unknown as Categories; // fix typescript error

  function startOfWeek(date: Date) {
    const diff = date.getDate() - date.getDay();
    return new Date(date.setDate(diff));
  }

  function endOfWeek(date: Date) {
    const diff = date.getDate() - date.getDay() + 6;
    return new Date(date.setDate(diff));
  }

  let pastWeekScores: ScoreSubmission[][] = []; // today last
  $: console.log(pastWeekScores);

  onMount(async () => {
    const now = new Date();
    const scores = await listScores({
      fromTime: startOfWeek(now).toISOString(),
      toTime: endOfWeek(now).toISOString(),
    });

    pastWeekScores = new Array(7)
      .fill([])
      .map((_, i) => {
        const day = new Date(now);
        day.setDate(day.getDate() - i + 1);
        return scores.filter((score) => {
          const scoreDate = new Date(Date.parse(score.submitted_at!));
          return (
            scoreDate.getDate() === day.getDate() &&
            scoreDate.getMonth() === day.getMonth() &&
            scoreDate.getFullYear() === day.getFullYear()
          );
        });
      })
      .reverse();
  });

  const data = pastWeekScores.map((scores, i) => {
      const day = new Date(now);
      day.setDate(day.getDate() - i + 1);
      const dateKey = `${(day.getMonth() + 1).toString().padStart(2, '0')}/${day.getDate().toString().padStart(2, '0')}/${day.getFullYear().toString().slice(-2)}`;
      return {"label": dateKey, "value": scores.length};
    });

  console.log(data[0]);

  const dataSource = {
    "chart": {
      "caption": "Countries With Most Oil Reserves [2022-23]",
      "subcaption": "In MMbbl = One Million barrels",
      "xaxisname": "Country",
      "yaxisname": "Reserves (MMbbl)",
      "numbersuffix": "K",
      "theme": "gammel"
    },
    "data": pastWeekScores.map((scores, i) => {
      const day = new Date(now);
      day.setDate(day.getDate() - i + 1);
      const dateKey = `${(day.getMonth() + 1).toString().padStart(2, '0')}/${day.getDate().toString().padStart(2, '0')}/${day.getFullYear().toString().slice(-2)}`;
      return {"label": dateKey, "value": scores.length};
    }),
  };
  const chartConfigs = {
    type: 'column2d',
    width: 600,
    height: 400,
    dataFormat: 'json',
    dataSource
  };
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

    <div class="stats-cards">
      <article>
        <hgroup>
          <h3>Streaks</h3>
          <p>Measure of how many days in a row you have completed your daily goal.</p>
        </hgroup>

        <SvelteFC {...chartConfigs} />

        <p>Current Streak: 0</p>
      </article>

      <article>
        <hgroup>
          <h3>Average Times</h3>
          <p>Measure of how long on average you took to solve a problem over time.</p>
        </hgroup>

        <p>Daily Average: 0</p>
      </article>
    </div>
  </section>
</WhitePage>

<style lang="scss">
  section {
    display: flex;
    flex-direction: column;
    margin: 1rem auto;
    width: 100%;
  }

  section.container {
    align-items: baseline;
  }

  .stats-cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    grid-gap: 1rem;
    width: 100%;

    article {
      padding: 1rem;
      border: 1px solid var(--primary);
      border-radius: 15px;

      h3 {
        margin: 0.5rem 0;
      }

      hgroup {
        border-bottom: 1px solid rgba(var(--primary-rgb), 0.25);
        p {
          margin-top: 0;
          font-size: 0.9rem;
        }
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
