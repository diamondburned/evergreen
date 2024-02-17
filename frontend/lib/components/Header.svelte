<script lang="ts">
  import { page } from "$app/stores";
</script>

<header class="container">
  <nav>
    <ul>
      <li>
        <a class="primary-text brand-text" href="/">Evergreen</a>
      </li>
    </ul>

    <ul>
      <li>
        <a
          class="on-background-text"
          class:active={$page.url.pathname == "/dashboard"}
          role="button"
          href="/dashboard">Dashboard</a
        >
      </li>
      <li>
        <a
          class="on-background-text"
          class:active={$page.url.pathname == "/settings"}
          role="button"
          href="/settings">Settings</a
        >
      </li>
    </ul>
  </nav>
</header>

<style lang="scss">
  .brand-text {
    font-size: 1.25em;
  }

  nav {
    display: flex;
    justify-content: space-between;
    width: 100%;
    font-weight: 400;

    margin: 1rem;
    border: 1px solid var(--md-sys-color-outline);
    border-radius: var(--border-radius);

    li {
      display: inline;
      padding-right: 50px;
    }

    a {
      text-decoration: none;
      transition: color 0.1s ease-in-out;

      &.active {
        color: var(--md-sys-color-primary);
        font-weight: 700;
      }

      &:hover {
        color: var(--md-sys-color-primary);
      }
    }
  }
</style>
