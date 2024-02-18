<script>
  import LoadingDots from "$lib/components/LoadingDots.svelte";
  import WhitePage from "$lib/components/WhitePage.svelte";
  import { fade } from "svelte/transition";
  import { cubicOut } from "svelte/easing";

  let loading = true;
</script>

<WhitePage>
  <main class="game-container" class:loading>
    {#if loading}
      <div class="loading-box" out:fade={{ easing: cubicOut, duration: 150 }}>
        <LoadingDots padded />
      </div>
    {/if}
    <iframe src="/dashboard" title="Unity game" on:load={() => (loading = false)} />
  </main>
</WhitePage>

<style lang="scss">
  .game-container {
    --aspect-ratio: 16 / 9;

    height: 100%;
    overflow: hidden;
    background-color: var(--background);

    position: relative;

    .loading-box {
      position: absolute;
      width: 100%;
      height: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    iframe {
      width: 100%;
      max-height: 100%;
      aspect-ratio: var(--aspect-ratio);
      border: none;

      position: relative;
      box-shadow: 0 0 10px 0 var(--background) inset;

      opacity: 1;
      transition: opacity 0.2s ease-in-out;
    }

    &.loading iframe {
      opacity: 0;
    }
  }
</style>
