<script lang="ts">
  import { isLoggedIn } from "$lib/api";
  import "normalize.css/normalize.css";
  import "$lib/styles/material-css/theme.css";
  import "$lib/styles/main.scss";
</script>

<header class="container">
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

<main class="container">
  <slot />
</main>
