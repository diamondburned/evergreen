<script lang="ts">
  import NavBar from "$lib/components/NavBar.svelte";
  import WhitePage from "$lib/components/WhitePage.svelte";
  import Roadmap from "$lib/components/roadmap/Roadmap.svelte";
  import categories from "$lib/categories.json";
</script>

<svelte:head>
  <title>Dashboard</title>
</svelte:head>

<WhitePage>
  <header class="container">
    <NavBar />
  </header>

  <section class="container roadmap-section">
    <h2>Study Plan</h2>
    <Roadmap {categories} />
  </section>

  <section class="container">
    <h2>Dashboard</h2>

    <div class="stats-cards">
      <article>
        <header>
          <h3>Streaks</h3>
          <p>Streaks are a measure of how many days in a row you have completed your daily goal.</p>
        </header>

        <p>Current Streak: 0</p>
      </article>

      <article>
        <header>
          <h3>Daily Average</h3>
          <p>How many days you have completed your daily goal on average.</p>
        </header>

        <p>Daily Average: 0</p>
      </article>
    </div>
  </section>
</WhitePage>

<style lang="scss">
  header {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    position: sticky;
    top: 0;

    background-color: rgba(var(--background-rgb), 0.85);
    backdrop-filter: blur(10px);
  }

  section {
    display: flex;
    flex-direction: column;
    margin-top: 1rem;
  }

  section.container {
    align-items: baseline;
  }

  .stats-cards {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    width: 100%;

    article {
      padding: 1rem;
      border: 1px solid var(--primary);
      border-radius: 15px;

      h3 {
        margin: 0.5rem 0;
      }

      header {
        border-bottom: 1px solid rgba(var(--primary-rgb), 0.25);
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
