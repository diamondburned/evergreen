<script lang="ts" context="module">
  declare global {
    interface Window {
      createUnityInstance: any;
    }
  }
</script>

<script lang="ts">
  import LoadingDots from "$lib/components/LoadingDots.svelte";
  import WhitePage from "$lib/components/WhitePage.svelte";
  import { fade } from "svelte/transition";
  import { onDestroy, onMount } from "svelte";
  import { cubicOut } from "svelte/easing";

  import webGLLoader from "$lib/../game/WebGL.loader.js?url";
  import webGLData from "$lib/../game/WebGL.data.br?url";
  import webGLCode from "$lib/../game/WebGL.wasm.br?url";
  import webGLFramework from "$lib/../game/WebGL.framework.js.br?url";
  import NavBar from "$lib/components/NavBar.svelte";

  let loading = true;
  let canvas: HTMLCanvasElement;

  const config = {
    loaderUrl: webGLLoader,
    dataUrl: webGLData,
    frameworkUrl: webGLFramework,
    codeUrl: webGLCode,
    streamingAssetsUrl: "StreamingAssets",
    companyName: "Company",
    productName: "Evergreen",
    productVersion: "0.1",
    showBanner: (msg: unknown, type: unknown) => {
      console.log(msg, type);
    },
  };
  console.log(config);

  let script: HTMLScriptElement;
  onMount(() => {
    script = document.createElement("script");
    script.src = config.loaderUrl;
    script.onload = async () => {
      try {
        await window.createUnityInstance(canvas, config, () => {});
        loading = false;
      } catch (err) {
        console.error(err);
        alert("An error occurred while loading the game :(");
      }
    };
    document.body.appendChild(script);
  });
  onDestroy(() => {
    if (script) {
      document.body.removeChild(script);
    }
  });
</script>

<WhitePage>
  <header slot="header">
    <NavBar container forceReload />
  </header>

  <main class="game-container" class:loading>
    {#if loading}
      <div class="loading-box" out:fade={{ easing: cubicOut, duration: 150 }}>
        <LoadingDots padded />
      </div>
    {/if}

    <canvas id="unity-canvas" width="1280" height="720" bind:this={canvas} />
  </main>
</WhitePage>

<style lang="scss">
  #unity-canvas {
    --scale: 0.8;

    max-width: calc(1280px * var(--scale));
    max-height: calc(720px * var(--scale));

    width: 100%;
    height: auto;
    margin: auto;
    aspect-ratio: 16/9;

    opacity: 1;
    transition: opacity 0.2s ease-in-out;
  }

  .game-container {
    --aspect-ratio: 16 / 9;

    height: 100%;
    overflow: hidden;
    background-color: var(--background);

    display: flex;
    position: relative;

    .loading-box {
      position: absolute;
      width: 100%;
      height: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    &.loading #unity-canvas {
      opacity: 0;
    }
  }
</style>
