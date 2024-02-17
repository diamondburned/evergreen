<script lang="ts">
  import { fly } from "svelte/transition";
  import { isAuthorized } from "$lib/api";

  import Hero from "$lib/components/Hero.svelte";
  import LoadingDots from "$lib/components/LoadingDots.svelte";
</script>

<svelte:head>
  <title>Home</title>
</svelte:head>

<Hero>
  <div class="content">
    <h1 class="brand">Evergreen</h1>
    <div class="bottom">
      {#if !$isAuthorized}
        <div out:fly={{ y: -30, duration: 500 }}>
          <LoadingDots dotSize={24} distance={32} />
        </div>
      {:else}
        <div in:fly={{ y: 30, duration: 500, delay: 500 }}>
          <button class="on-secondary-text">Play</button>
          <p class="login">Already played? <a href="/login">Sign In</a></p>
        </div>
      {/if}
    </div>
  </div>
</Hero>

<style lang="scss">
  .content {
    gap: 1rem;
  }

  .content,
  .content > div {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }

  .bottom {
    height: 6rem;
  }

  h1 {
    font-size: 5em;
    text-shadow: 2px 2px 2px black;
    margin: 1rem;
  }

  button {
    padding: 0.75em;
    width: 300px;
    max-width: 100%;

    font-size: 22px;

    border: none;
    border-radius: 15px;
    transition: all 0.15s ease-in-out;

    &:hover {
      box-shadow: 0 0.5em 1.2em -1em var(--md-sys-color-shadow);
      transform: translateY(-0.1em);
    }

    &:active {
      transform: translateY(0);
    }
  }

  p.login {
    margin: 1rem;
    text-align: center;
    font-weight: 400;

    a {
      color: inherit;
      text-decoration: underline;
      font-weight: 600;
    }
  }
</style>
