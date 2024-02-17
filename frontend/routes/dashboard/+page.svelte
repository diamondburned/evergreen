<script lang="ts">
  import NavBar from "$lib/components/NavBar.svelte";
  import WhitePage from "$lib/components/WhitePage.svelte";

  const categories = {
    "probability-statistics": {
      label: "Probability & Statistics",
      levels: ["Combinatorics", "Regression", "Bayesian Statistics"],
    },
    "data-structures": {
      label: "Data Structures",
      levels: ["Arrays", "Binary Trees", "Linked Lists"],
    },
    "object-oriented-programming": {
      label: "Object-Oriented Programming",
      levels: ["Classes", "Polymorphism", "Design Patterns"],
    },
    algorithms: {
      label: "Algorithms",
      levels: ["Binary Search", "Dijkstra's", "NP-Complete"],
    },
    "dynamic-programming": {
      label: "Dynamic Programming",
      levels: ["Fibonacci Sequence", "Memoization", "State Machine Optimization"],
    },
    "machine-learning": {
      label: "Machine Learning",
      levels: ["Decision Tree", "Dimensionality Reduction", "Neural Networks"],
    },
  };

  let currentCategory = "probability-statistics";
</script>

<svelte:head>
  <title>Dashboard</title>
</svelte:head>

<WhitePage>
  <header class="container">
    <NavBar />
  </header>

  <section>
    <h2 class="container">Study Plan</h2>

    <aside>
      <ul>
        {#each Object.entries(categories) as [name, category]}
          <li>
            <a
              href="#"
              class:active={currentCategory == name}
              on:click|preventDefault={() => (currentCategory = name)}
            >
              {category.label}
            </a>
          </li>
        {/each}
      </ul>
    </aside>

    <div class="roadmap"></div>
  </section>

  <section class="container">
    <h2>Dashboard</h2>

    <div class="stats-cards">
      <section>
        <header>
          <h3>Streaks</h3>
          <p>Streaks are a measure of how many days in a row you have completed your daily goal.</p>
        </header>

        <p>Current Streak: 0</p>
      </section>

      <section>
        <header>
          <h3>Daily Average</h3>
          <p>How many days you have completed your daily goal on average.</p>
        </header>

        <p>Daily Average: 0</p>
      </section>
    </div>
  </section>
</WhitePage>

<style lang="scss">
  header {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }

  section {
    display: flex;
    flex-direction: column;
  }

  section.container {
    align-items: baseline;
  }

  .stats-cards {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    width: 100%;

    section {
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
</style>
