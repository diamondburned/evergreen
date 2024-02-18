<script>
  import WhitePage from "$lib/components/WhitePage.svelte";
</script>

<WhitePage>
  <main class="game-container">
    <iframe src="/dashboard" title="Codingame" />
  </main>
</WhitePage>

<style lang="scss">
  .game-container {
    --aspect-ratio: 16 / 9;

    height: 100%;
    overflow: hidden;
    background-color: var(--background);

    iframe {
      width: 100%;
      max-height: 100%;
      aspect-ratio: var(--aspect-ratio);
      border: none;

      position: relative;
      box-shadow: 0 0 10px 0 var(--background) inset;
    }
  }
</style>
