<script lang="ts">
  export let error: string | undefined = undefined;
</script>

{#if error}
  <p class="error">{error}</p>
{/if}

<style lang="scss">
  .error {
    color: var(--md-sys-color-error);
    margin: 0;
    text-align: left;
    background: none;

    &::before {
      content: "Error: ";
      font-weight: 700;
    }
  }
</style>
