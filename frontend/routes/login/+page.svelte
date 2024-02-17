<script lang="ts">
  import { isLoggedIn, token, login, register } from "$lib/api";
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
    switch (action) {
      case "login":
        session = await login({ email, password });
        break;
      case "register":
        session = await register({ email, password });
        break;
    }
    console.log(session);
    $token = session.token;
  }
</script>

<svelte:head>
  <title>Register</title>
</svelte:head>

<article>
  <header>
    <hgroup>
      <h2>Login</h2>
    </hgroup>
  </header>

  <form>
    <fieldset>
      <label>
        Email
        <input type="email" bind:value={email} />
      </label>

      <label>
        Password
        <input type="password" bind:value={password} />
      </label>
    </fieldset>

    <div role="group">
      <button disabled={!valid} on:click={() => submit("login")}> Login </button>
      <button disabled={!valid} class="secondary" on:click={() => submit("register")}>
        Register
      </button>
    </div>
  </form>
</article>

<style lang="scss">
  article {
    max-width: 400px;
    margin: auto;
  }
</style>
