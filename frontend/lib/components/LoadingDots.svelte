<script lang="ts">
  export let dotSize = 16;
  export let distance = 12;
  export let duration = "1s";
  export let padded = false;
</script>

<div
  class="loading-dots"
  class:padded
  style="--dot-size: {dotSize}px; --distance: {distance}px; --duration: {duration};"
>
  <span class="loader"></span>
</div>

<style lang="scss">
  .loading-dots {
    --distance-u: calc(-1 * var(--distance) / 2);
    --distance-d: calc(+1 * var(--distance) / 2);
    --gap-size: calc(var(--dot-size) / 6 * 7);

    width: calc(var(--dot-size) * 4 + var(--gap-size) * 3);
    height: calc(var(--dot-size) * 2 + var(--distance));

    &.padded {
      min-height: 20vh;
      display: flex;
      align-items: center;
      margin: auto;
    }
  }

  .loader {
    margin-left: calc(3 * var(--dot-size) + 1.5 * var(--dot-size));
    margin-top: calc(var(--distance));

    width: var(--dot-size);
    height: var(--dot-size);
    display: block;
    border-radius: 50%;
    animation: animloader var(--duration) ease-in-out infinite alternate;
  }

  @keyframes animloader {
    0% {
      box-shadow:
        calc(-3 * var(--gap-size)) var(--distance-u),
        calc(-1 * var(--gap-size)) var(--distance-d),
        calc(+1 * var(--gap-size)) var(--distance-u);
    }
    33% {
      box-shadow:
        calc(-3 * var(--gap-size)) var(--distance-d),
        calc(-1 * var(--gap-size)) var(--distance-u),
        calc(+1 * var(--gap-size)) var(--distance-d);
    }
    66% {
      box-shadow:
        calc(-3 * var(--gap-size)) var(--distance-u),
        calc(-1 * var(--gap-size)) var(--distance-d),
        calc(+1 * var(--gap-size)) var(--distance-u);
    }
    100% {
      box-shadow:
        calc(-3 * var(--gap-size)) var(--distance-d),
        calc(-1 * var(--gap-size)) var(--distance-u),
        calc(+1 * var(--gap-size)) var(--distance-d);
    }
  }
</style>
