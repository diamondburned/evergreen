<script lang="ts">
  import { afterUpdate, onDestroy, onMount, tick } from "svelte";

  export let label: string;
  export let description: string;
  export let flip: boolean = false;

  // Deal with the consequences of our sin: by abusing an SVG for the roadmap.
  // Because HTML elements within a foreignObject use their own coordinate
  // system, none of the tooltip libraries work. So we have to do it manually.
  let tooltipElement: HTMLElement;
  let nodeElement: HTMLElement;
  let scrollY: number;

  function update() {
    const rect = nodeElement.getBoundingClientRect();
    const anchorX = rect.x + rect.width / 2;
    const anchorY = rect.y + rect.height / 2;
    console.log(rect, anchorX, anchorY);

    tooltipElement.style.setProperty("--anchor-x", `${anchorX}px`);
    tooltipElement.style.setProperty("--anchor-y", `${anchorY}px`);

    const tooltipW = tooltipElement.offsetWidth;
    const top = anchorY + rect.height / 2;
    const left = anchorX - tooltipW / 2;

    tooltipElement.style.setProperty("--top", `${top}px`);
    tooltipElement.style.setProperty("--left", `${left}px`);
  }

  afterUpdate(update);
  setTimeout(update, 100); // hack lmao
  $: {
    scrollY;
    nodeElement && update();
  }

  let observer: ResizeObserver;

  onMount(() => {
    tooltipElement = document.createElement("p");
    tooltipElement.classList.add("roadmap-tooltip");
    tooltipElement.textContent = description;

    document.body.appendChild(tooltipElement);

    observer = new ResizeObserver(update);
    observer.observe(nodeElement);

    update();
  });

  onDestroy(() => {
    document.body.removeChild(tooltipElement);
    observer.disconnect();
  });
</script>

<svelte:window bind:scrollY />

<p
  class="node"
  class:flip
  data-description={description}
  bind:this={nodeElement}
  on:mouseenter={() => tooltipElement.classList.add("visible")}
  on:mouseleave={() => tooltipElement.classList.remove("visible")}
>
  {label}
</p>

<style lang="scss">
  p.node {
    width: fit-content;
    margin: auto;
    border: 2px solid var(--primary);
    border-radius: 15px;
    padding: 0.45rem 1.5rem;

    transition: all 0.1s ease-in-out;

    &:hover {
      background-color: var(--primary);
      color: var(--background);
      cursor: help;
    }

    &.flip {
      transform: rotateY(180deg);
    }
  }

  :global(.roadmap-tooltip) {
    display: block;

    opacity: 0;
    pointer-events: none;
    transition: all 0.075s ease-in-out;

    --top-offset: -5px;
    transform: translateY(var(--top-offset));

    width: 15rem;
    height: auto;

    position: fixed;
    top: calc(var(--top) + 0rem);
    left: var(--left);

    background-color: var(--background);
    border: 1px solid var(--primary);
    border-radius: 15px;
    padding: 0.75rem;

    &::before {
      content: "";
      position: absolute;
      border-bottom: 10px solid var(--primary);
      border-left: 8px solid transparent;
      border-right: 8px solid transparent;
      top: -10px;
      left: calc(50% - 8px);
    }
  }

  :global(.roadmap-tooltip.visible) {
    opacity: 1;
    pointer-events: auto;
    --top-offset: 0;
  }
</style>
