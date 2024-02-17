<script lang="ts">
  import { cubicOut, cubicIn } from "svelte/easing";
  import { fly } from "svelte/transition";
  import SVG from "$lib/components/roadmap/SVG.svelte";
  import RoadmapButton from "$lib/components/roadmap/RoadmapButton.svelte";

  type CategoryLevel = {
    label: string;
    description: string;
  };

  type Categories = Record<
    string,
    {
      label: string;
      levels: [CategoryLevel, CategoryLevel, CategoryLevel];
    }
  >;

  export let categories: Categories = {};
  export let currentCategory = Object.keys(categories)[0]!;

  const duration = 150;
  const delay = 20;
  const y = 50;

  const transitionIn = { easing: cubicOut, y, duration, delay: duration + delay };
  const transitionOut = { easing: cubicIn, y: -y, duration };

  $: flip = Object.keys(categories).indexOf(currentCategory) % 2 === 0;
  $: levels = categories[currentCategory]!.levels;
</script>

<div class="roadmap">
  <aside class="sidebar">
    <ul>
      {#each Object.entries(categories) as [name, category]}
        <li>
          <a
            href={"#"}
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
        <SVG>
          <div class="contents" slot="1">
            <RoadmapButton label={levels[0].label} description={levels[0].description} {flip} />
          </div>
          <div class="contents" slot="2">
            <RoadmapButton label={levels[1].label} description={levels[1].description} {flip} />
          </div>
          <div class="contents" slot="3">
            <RoadmapButton label={levels[2].label} description={levels[2].description} {flip} />
          </div>
        </SVG>
      </div>
    {/key}
  </div>
</div>

<style lang="scss">
  .contents {
    display: contents;
  }

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
      }
    }
  }

  .sidebar {
    width: 20rem;
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
