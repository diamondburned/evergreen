<script lang="ts">
  import { cubicOut, cubicIn } from "svelte/easing";
  import { fly } from "svelte/transition";
  import { tooltip } from "@svelte-plugins/tooltips";
  import RoadmapSVG from "$lib/components/RoadmapSVG.svelte";

  type Categories = Record<
    string,
    {
      label: string;
      levels: {
        label: string;
        description: string;
      }[];
    }
  >;

  export let categories: Categories = {};
  export let currentCategory = Object.keys(categories)[0];

  const duration = 150;
  const delay = 20;
  const y = 50;

  const transitionIn = { easing: cubicOut, y, duration, delay: duration + delay };
  const transitionOut = { easing: cubicIn, y: -y, duration };

  $: flip = Object.keys(categories).indexOf(currentCategory) % 2 === 0;
  $: levels = categories[currentCategory].levels;
</script>

<div class="roadmap">
  <aside class="sidebar">
    <ul>
      {#each Object.entries(categories) as [name, category]}
        <li>
          <a
            href="#"
            class:active={currentCategory == name}
            on:click|preventDefault={() => (currentCategory = name)}
          >
            {category.label}
          </a>
        </li>
      {/each}
    </ul>
  </aside>

  <div class="roadmap-container">
    {#key currentCategory}
      <div class="roadmap-box" class:flip in:fly={transitionIn} out:fly={transitionOut}>
        <RoadmapSVG>
          <p
            class="node"
            slot="1"
            use:tooltip={{
              action: "hover",
              content: levels[0].description,
              autoPosition: true,
              delay: 0,
            }}
          >
            {levels[0].label}
          </p>
          <p
            class="node"
            slot="2"
            use:tooltip={{
              action: "hover",
              content: levels[1].description,
              autoPosition: true,
              delay: 0,
            }}
          >
            {levels[1].label}
          </p>
          <p
            class="node"
            slot="3"
            use:tooltip={{
              action: "hover",
              content: levels[2].description,
              autoPosition: true,
              delay: 0,
            }}
          >
            {levels[2].label}
          </p>
        </RoadmapSVG>
      </div>
    {/key}
  </div>
</div>

<style lang="scss">
  .roadmap {
    display: flex;
    flex-direction: row;
    width: 100%;

    .roadmap-container {
      width: 100%;
      height: 560px;
    }

    .roadmap-box {
      display: flex;
      align-items: center;
      justify-content: center;

      &.flip {
        transform: rotateY(180deg);

        p.node {
          transform: rotateY(180deg);
        }
      }
    }

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
    }
  }

  .sidebar {
    width: 50%;
    height: fit-content;
    border-right: 1px solid rgba(var(--primary-rgb), 0.25);
    margin-top: 1rem;
    padding-right: 1rem;

    ul {
      list-style: none;
      text-align: right;
    }

    a {
      color: inherit;
      padding: 0.5rem 0.25rem;
      display: block;
      text-decoration: none;

      opacity: 0.65;
      transition: all 0.1s ease-in-out;

      &:hover {
        opacity: 1;
      }

      &.active {
        font-weight: 700;
        opacity: 1;
        color: var(--primary);

        &::before {
          content: "● ";
          position: absolute;
          left: 1.25rem;
          font-size: 1rem;
        }
      }
    }
  }
</style>
