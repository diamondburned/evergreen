<script lang="ts">
  import { onMount } from 'svelte';
	import NavBar from '$lib/components/NavBar.svelte';
	import WhitePage from '$lib/components/WhitePage.svelte';
  import { getSelf } from '$lib/api';

	let avatar_img = "/stock-avatar.jpeg";
  let avatar, fileinput;
  let display_name = "Eric Zhang";
  let email="ericzhang11@g.ucla.edu";

  onMount(async () => {
    let user = await getSelf();
    console.log("hi");
    console.log(user);
  })
  
</script>

<svelte:head>
  <title>Settings</title>
</svelte:head>

<WhitePage>
    <header class="container">
        <NavBar />
    </header>

    <section class="container">
      <h2>Settings</h2>

      <section class="settings">
        <div>
          <h3> Avatar </h3>
          <div class="user">
            <img src={avatar_img} class="avatar" alt="avatar"/>
            <input bind:this={avatar} type="file"/>
          </div>
        </div>
        <div>
          <label>
            <h3>Display Name</h3>
            <input>
          </label>
        </div>
        <div>
          <h3> Email: </h3>
          <div class="user">
            <p>{email}</p>
            <button class="hover">Change email</button>
          </div>
        </div>
        <div>
          <h3> Password: </h3>
          <div class="user">
            <p>********</p>
            <button class="hover">Change password</button>
          </div>
        </div>
      </section>

      <button class="hover">Save</button>
    </section>
</WhitePage>

<style lang="scss">
    header {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
    }
    section {
      display: flex;
      flex-direction: column;
    }
    section.container {
      align-items: baseline;
    }
    section.settings {
      width: 100%;
      padding: 1rem;
      border: 1px solid var(--primary);
      border-radius: 15px;

      h3 {
        margin: 0.5rem 0;
      }
      
      div {
        margin-bottom: 15px;
      }
      div.user {
        display: flex;
        align-items: center;
        justify-content: space-between;
      }
    }
    img.avatar {
      border-radius: 50%;
      width: 120px;
      margin-right: 20px;
    }
    input {
      margin-top: 0.25em;
      padding: 0.5em;
      border: 1px solid var(--primary);
      border-radius: 15px;
    }
    button {
      padding: 0.75em;
      width: 240px;
      max-width: 100%;

      font-size: 15px;

      border: none;
      border-radius: 15px;

      background-color: var(--primary);
      color: white;
    }
</style>