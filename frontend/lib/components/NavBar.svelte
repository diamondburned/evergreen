<script lang="ts">
  import { page } from "$app/stores";

  export let navigation = [
    {
      path: "/dashboard",
      label: "Dashboard",
    },
    {
      path: "/settings",
      label: "Settings",
    },
  ];
</script>

<nav>
  <ul>
    <li>
      <a class="primary-text brand" href="/">
        <img class="logo" src="/logo-small.png" alt="Evergreen Logo" />
        Evergreen
      </a>
    </li>
  </ul>

  <ul>
    {#each navigation as { path, label }}
      <li>
        <a
          class="on-background-text"
          class:active={$page.url.pathname == path}
          role="button"
          href={path}
        >
          {label}
        </a>
      </li>
    {/each}
  </ul>
</nav>

<style lang="scss">
  nav {
    display: flex;
    justify-content: space-between;
    width: 100%;
    font-weight: 400;

    z-index: 100;

    ul:nth-child(2) {
      height: fit-content;
      margin: auto 0;
    }

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

    .brand {
      font-size: 1.5em;

      .logo {
        width: 2.25rem;
        margin-right: 0.25rem;
        vertical-align: bottom;
      }
    }
  }
</style>
