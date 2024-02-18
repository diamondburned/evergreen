<script lang="ts" context="module">
  export type CategoryLevel = {
    label: string;
    description: string;
  };

  export type Categories = Record<
    string,
    {
      label: string;
      levels: [CategoryLevel, CategoryLevel, CategoryLevel];
    }
  >;
</script>

<script lang="ts">
  import { cubicOut, cubicIn } from "svelte/easing";
  import { fly } from "svelte/transition";
  import SVG from "$lib/components/roadmap/SVG.svelte";
  import RoadmapButton from "$lib/components/roadmap/RoadmapButton.svelte";
  import { GameDifficulty, recommendDifficulty } from "$lib/api";

  export let categories: Categories = {};
  export let currentCategory = Object.keys(categories)[0]!;

  const duration = 150;
  const delay = 20;
  const y = 50;

  const transitionIn = { easing: cubicOut, y, duration, delay: duration + delay };
  const transitionOut = { easing: cubicIn, y: -y, duration };

  $: flip = Object.keys(categories).indexOf(currentCategory) % 2 === 0;
  $: levels = categories[currentCategory]!.levels;

  let predictions: Record<keyof Categories, GameDifficulty> = {};
  async function loadPrediction(category: keyof Categories) {
    if (predictions[category] == undefined) {
      try {
        predictions[category] = await recommendDifficulty(category);
        predictions = { ...predictions }; // force reactivity
      } catch (err) {
        console.error(err);
      }
    }
  }

  $: loadPrediction(currentCategory);
  $: currentPrediction = predictions[currentCategory];
  $: currentPredictionReady = currentPrediction != undefined;
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
      <div
        class="roadmap-box"
        class:flip
        class:recommends-slot-1={currentPrediction == GameDifficulty.Intermediate}
        class:recommends-slot-2={currentPrediction == GameDifficulty.Advanced}
        class:loading-recommendation={!currentPredictionReady}
        in:fly={transitionIn}
        out:fly={transitionOut}
      >
        <SVG>
          <div
            class="contents"
            class:recommended={currentPrediction == GameDifficulty.Beginner}
            slot="1"
          >
            <RoadmapButton
              slot={1}
              label={levels[0].label}
              description={levels[0].description}
              recommended={currentPrediction == GameDifficulty.Beginner}
              {flip}
            />
          </div>
          <div
            class="contents"
            class:recommended={currentPrediction == GameDifficulty.Intermediate}
            slot="2"
          >
            <RoadmapButton
              slot={2}
              label={levels[1].label}
              description={levels[1].description}
              recommended={currentPrediction == GameDifficulty.Intermediate}
              {flip}
            />
          </div>
          <div
            class="contents"
            class:recommended={currentPrediction == GameDifficulty.Advanced}
            slot="3"
          >
            <RoadmapButton
              slot={3}
              label={levels[2].label}
              description={levels[2].description}
              recommended={currentPrediction == GameDifficulty.Advanced}
              {flip}
            />
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

      :global(.slot-1-path),
      :global(.slot-2-path) {
        transition: all 0.15s ease-in-out;
      }

      &.loading-recommendation {
        @keyframes breathing {
          0% {
            fill: rgba(var(--primary-rgb), 0.15);
          }
          50% {
            fill: rgba(var(--primary-rgb), 0.35);
          }
        }

        :global(.slot-1-path),
        :global(.slot-2-path) {
          animation: breathing 0.5s infinite alternate;
        }
      }

      &:not(.loading-recommendation) {
        :global(.slot-1-path),
        :global(.slot-2-path) {
          animation: none;
          fill: rgba(var(--primary-rgb), 0.35);
        }

        &.recommends-slot-1 :global(.slot-1-path),
        &.recommends-slot-2 :global(.slot-1-path),
        &.recommends-slot-2 :global(.slot-2-path) {
          fill: var(--primary);
          filter: drop-shadow(0 0 5px rgba(var(--primary-rgb), 0.5));
        }
      }
    }
  }

  .sidebar {
    width: 22rem;
    height: fit-content;
    border-right: 1px solid rgba(var(--primary-rgb), 0.25);
    margin: auto;
    padding: 2rem 0;
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
      position: relative;

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
          left: -1.25rem;
          font-size: 1rem;
        }
      }
    }
  }
</style>
