<script lang="ts">
  import WhitePage from "$lib/components/WhitePage.svelte";
  import Roadmap from "$lib/components/roadmap/Roadmap.svelte";
  import categories_ from "$lib/categories.json";
  import { type Categories } from "$lib/components/roadmap/Roadmap.svelte";

  $: categories = categories_ as unknown as Categories; // fix typescript error
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
