<script lang="ts">
  import Hero from "$lib/components/Hero.svelte";
</script>

<svelte:head>
  <title>Home</title>
</svelte:head>

<Hero>
  <div class="content">
    <h1 class="brand">Evergreen</h1>
    <button><p class="on-secondary-text">Play</p></button>
    <h3>Already played? <a href="/login">Login</a></h3>
  </div>
</Hero>

<style lang="scss">
  .content {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    gap: 1rem;
  }

  h1 {
    font-size: 5em;
    text-shadow: 2px 2px 2px black;
    margin: 1rem;
  }

  button {
    padding: 0.75em;
    width: 300px;
    max-width: 90%;

    border: none;
    border-radius: 15px;
    transition: all 0.15s linear;

    &:hover {
      box-shadow: 0 0.5em 0.5em -0.4em var(--md-sys-color-shadow);
    }

    p {
      font-size: 22px;
      margin: auto;
    }
  }

  h3 {
    margin: 0.5rem;
  }
</style>
