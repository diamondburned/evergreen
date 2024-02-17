<script lang="ts">
  import { isLoggedIn } from "$lib/api";
  import "normalize.css/normalize.css";
  import "$lib/styles/material-css/theme.css";
  import "$lib/styles/main.scss";
</script>

<svelte:head>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="" />
  <link
    href="https://fonts.googleapis.com/css2?family=Nunito:ital,wght@0,200..1000;1,200..1000&display=swap"
    rel="stylesheet"
  />
</svelte:head>

<header>
  <nav>
    <ul>
      <li><strong>PixieCode</strong></li>
    </ul>
    <ul>
      {#if !$isLoggedIn}
        <li>
          <a role="button" href="/login">Register</a>
        </li>
      {/if}
    </ul>
  </nav>
</header>

<slot />
