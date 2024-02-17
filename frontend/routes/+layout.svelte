<script lang="ts">
  import { isLoggedIn } from "$lib/api";
</script>

<svelte:head>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css" />
</svelte:head>

<header class="container">
  <nav>
    <ul>
      <li><strong>Demo App</strong></li>
    </ul>
    <ul>
      {#if !$isLoggedIn}
        <li>
          <a role="button" href="/login" class="secondary">Register</a>
        </li>
      {/if}
    </ul>
  </nav>
</header>

<main class="container">
  <slot />
</main>
