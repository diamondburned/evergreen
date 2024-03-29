<script lang="ts">
  import { onDestroy, onMount } from "svelte";

  export let label: string;
  export let description: string;
  export let slot: number;
  export let flip: boolean = false;
  export let recommended: boolean = false;

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

    tooltipElement.style.setProperty("--anchor-x", `${anchorX}px`);
    tooltipElement.style.setProperty("--anchor-y", `${anchorY}px`);

    const tooltipW = tooltipElement.offsetWidth;
    const top = anchorY + rect.height / 2;
    const left = anchorX - tooltipW / 2;

    tooltipElement.style.setProperty("--top", `${top}px`);
    tooltipElement.style.setProperty("--left", `${left}px`);
  }

  let interval: number;

  onMount(() => {
    tooltipElement = document.createElement("p");
    tooltipElement.classList.add("roadmap-tooltip");
    tooltipElement.textContent = description;

    document.body.appendChild(tooltipElement);
    interval = window.setInterval(() => update(), 1000);
    update();
  });

  onDestroy(() => {
    clearInterval(interval as number);
    document.body.removeChild(tooltipElement);
  });
</script>

<svelte:window bind:scrollY />

<p
  class="node"
  class:flip
  class:recommended
  data-slot={slot}
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
    padding: 0.45rem 1.15rem;
    position: relative;

    transition: all 0.1s ease-in-out;

    &:hover {
      background-color: var(--primary);
      color: var(--background);
      cursor: help;
    }

    &::before {
      content: attr(data-slot);
      display: block;
      position: absolute;
      left: -2rem;
      border: 1.5px solid var(--primary);
      border-radius: 50px;
      width: 1rem;
      height: 1rem;
      text-align: center;
      line-height: 1rem;
      font-size: 0.75rem;
      font-weight: 600;
      background-color: var(--background);
      color: var(--primary);
    }

    &.flip {
      transform: rotateY(180deg);
    }

    &.recommended::after {
      content: "⭐";
      position: absolute;
      right: -2rem;
      text-shadow: 0 0 10px gold;
    }
  }

  :global(p.roadmap-tooltip) {
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

  :global(p.roadmap-tooltip.visible) {
    opacity: 1;
    pointer-events: auto;
    --top-offset: 0;
  }
</style>
