<script lang="ts">
    import { isLoggedIn } from "$lib/api";
  </script>

<header class="container">
  <nav>
    <ul>
        <li><strong>
            <a class="primary-text" href="/">PixieCode</a>
        </strong></li>
        <li><strong>
            <a class="on-background-text" role="button" href="/">Dashboard</a>
        </strong></li>
        <li><strong>
            <a class="on-background-text" role="button" href="/">Settings</a>
        </strong></li>
    </ul>
  </nav>
  <br>
</header>

<style lang="scss">
    .container {
        height: 50px;
        display: flex;
        align-items: center;
    }
    li {
        display: inline;
        float: left;
        padding-right: 50px;
    }
    a {
        text-decoration: none;
    }
</style>
