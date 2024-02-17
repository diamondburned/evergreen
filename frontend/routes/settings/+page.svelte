<script lang="ts">
  import { onMount } from 'svelte';
	import NavBar from '$lib/components/NavBar.svelte';
	import WhitePage from '$lib/components/WhitePage.svelte';
  import { getAsset, uploadAsset, getSelf, updateSelf } from '$lib/api';

  let fileinput;
  let user, display_name, email, avatar_hash;
  let display_name_changed = false;
  let show_email_input = false;
  let show_password_input = false;

  async function setAvatar() {
    avatar_file = await uploadAsset();
    avatar_hash = avatar_file.hash;
    self.update();
  }

  function changeDisplayName() {
    display_name_changed = true;
  }

  function setDisplayName() {
    display_name_changed = false;
  }

  function toggleEmailInput() {
    show_email_input = ! show_email_input;
  }

  function togglePasswordInput() {
    show_password_input = ! show_password_input;
  }

  onMount(async () => {
    user = await getSelf();
    display_name = user.display_name;
    email = user.email;
    avatar_hash = user.avatar_hash;
    console.log(email, avatar_hash);
  });

  async function update() {
    let userUpdateObj = {
      display_name: display_name,
      email: email,
      avatar_hash: avatar_hash,
      password: password,
    };
    await updateSelf(userUpdateObj);
    user = await getSelf();
    console.log(user.display_name, user.email, user.password);
  }
  
</script>

<svelte:head>
  <title>Settings</title>
</svelte:head>

<WhitePage>
    <header class="container">
        <NavBar />
    </header>

    <form class="container" on:submit={update}>
      <h2>Settings</h2>

      <section class="settings">
        <div>
          <h3> Avatar </h3>
          <div class="user">
            <img src="/stock-avatar.jpeg" class="avatar" alt="avatar"/>
            <input bind:this={avatar_hash} type="file" accept=".jpg, jpeg, .png, .webp"/>
          </div>
        </div>
        <div>
          <h3>Display Name</h3>
          <div class="user">
            <input bind:value={display_name} on:input={changeDisplayName}>
            {#if display_name_changed}
            <button class="hover" type="submit" on:click={setDisplayName}>
              Save
            </button>
            {/if}
          </div>
        </div>
        <div>
          <h3> Email: </h3>
          <div class="user">
            {#if show_email_input}
               <input bind:value={email}>
            {:else}
              <p>{email}</p>
            {/if}
            <button class="hover" type="submit" on:click={toggleEmailInput}>
              {#if show_email_input}
                Save
              {:else}
                Change email
              {/if}
            </button>
          </div>
        </div>
        <div>
          <h3> Password: </h3>
          <div class="user">
            {#if show_password_input}
              <div class="change-password">
                <p>Old Password</p>
                <input>
                <p>New Password</p>
                <input>
                <p>Confirm New Password</p>
                <input>
              </div>
            {:else}
              <p>********</p>
            {/if}
            <button class="hover" type="submit" on:click={togglePasswordInput}>
              {#if show_password_input}
                Save
              {:else}
                Change password
              {/if}
            </button>
          </div>
        </div>
      </section>
    </form>
</WhitePage>

<style lang="scss">
    header {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
    }
    form {
      display: flex;
      flex-direction: column;
    }
    form.container {
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
        margin-bottom: 36px;
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
    div.change-password {
      display: flex;
      flex-direction: column;
      * {
        margin-bottom: 0.25em;
      }
    }
</style>