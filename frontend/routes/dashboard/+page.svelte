<script lang="ts">
  import NavBar from "$lib/components/NavBar.svelte";
</script>

<svelte:head>
  <title>Dashboard</title>
</svelte:head>

<header class="container">
  <NavBar />
</header>

<main class="container">
  <header>
    <h1>Dashboard</h1>
  </header>

  <div class="cards">
    <section>
      <h2>Streaks</h2>
    </section>

    <section></section>
  </div>
</main>

<style lang="scss">
  main {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }
</style>
