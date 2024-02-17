<script lang="ts">
	// import { PageData } from './../../../.svelte-kit/types/frontend/routes/$types.d.ts';
	import Hero from './../../lib/components/Hero.svelte';
  import { isLoggedIn, token, login } from "$lib/api";
  import { goto } from "$app/navigation";

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
  <article>
    <form>
        <label> Email*</label> <br>
        <input type="email" bind:value={email} />
        <br>
        <label> Password*</label> <br>
        <input type="password" bind:value={password} />
      <div role="group">
        <button disabled={!valid} on:click={() => submit("login")}> Sign In </button>
      </div>
    </form>
  </article>
</Hero>

<style lang="scss">
  article {
    max-width: 400px;
    margin: auto;
  }
  header {
    text-align: center;
  }
  h1 {
    font-size: 4em;
    text-shadow: 2px 2px 2px black;
  }
  label {
    font-size: 20px;
  }
  input {
    padding: 0.5em;
    font-size: 1.25em;
    margin-bottom: 36px;
    margin-top: 10px;
    border-radius: 20px;
    width: 300px;
  }
  div[role=group] {
    margin-top: 36px;
    text-align: center;
  }
  button {
    padding: 0.75em;
    width: 180px;
    max-width: 90%;

    border: none;
    border-radius: 20px;
    transition: all 0.15s linear;

    &:hover {
      box-shadow: 0 0.5em 0.5em -0.4em var(--md-sys-color-shadow);
    }
  }
</style>
