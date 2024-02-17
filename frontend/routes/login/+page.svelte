<script lang="ts">
  // import { PageData } from './../../../.svelte-kit/types/frontend/routes/$types.d.ts';
  import Hero from "./../../lib/components/Hero.svelte";
  import { isLoggedIn, token, login } from "$lib/api";
  import { goto } from "$app/navigation";
  import NavBar from "$lib/components/NavBar.svelte";

  $: {
    if ($isLoggedIn) {
      goto("/");
    }
  }

  let email = "";
  let password = "";

  $: valid = email && password;

  async function submit(action: "login" | "register") {
    let session;
    session = await login({ email, password });
    console.log(session);
    $token = session.token;
  }
</script>

<svelte:head>
  <title>Login</title>
</svelte:head>

<Hero>
  <header>
    <NavBar navigation={[]} />
  </header>

  <main>
    <form>
      <label>
        Email
        <input type="email" bind:value={email} />
      </label>
      <label>
        Password
        <input type="password" bind:value={password} />
      </label>
      <button class="floaty inverted" disabled={!valid} on:click={() => submit("login")}>
        Sign in
      </button>
    </form>
  </main>
</Hero>

<style lang="scss">
  main,
  form {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  main,
  header {
    position: absolute;
  }

  main {
    width: 100%;
    height: 100%;
  }

  form {
    gap: 2rem;

    label {
      width: 100%;
      max-width: 300px;

      display: flex;
      flex-direction: column;

      font-size: 0.95em;
      font-weight: 700;
      font-family: "Linotte", sans-serif;

      input {
        margin-top: 0.25em;
        padding: 0.5em;
        border: 1px solid var(--primary);
        border-radius: 15px;
      }
    }

    button {
      padding: 0.5em 2em;

      border-radius: 15px;
      transition: all 0.15s linear;

      &:hover {
        box-shadow: 0 0.5em 0.5em -0.4em var(--md-sys-color-shadow);
      }
    }
  }
</style>
