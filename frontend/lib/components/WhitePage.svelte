<script lang="ts">
  import NavBar from "./NavBar.svelte";

  let scrollY = 0;
  $: scrolled = scrollY > 5;
</script>

<svelte:window bind:scrollY />

<div class="white-page" class:scrolled>
  <slot name="header">
    <header>
      <NavBar container />
    </header>
  </slot>

  <slot />
</div>

<style lang="scss">
  .white-page {
    width: 100%;
    min-height: 100%;
    background-color: var(--background);

    & > :global(header) {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      position: sticky;
      top: 0;
      z-index: 100;

      background-color: rgba(var(--background-rgb), 0.75);
      backdrop-filter: blur(6px);

      transition: all 0.2s ease-in-out;
    }

    &.scrolled > :global(header) {
      box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.1);
    }
  }
</style>
