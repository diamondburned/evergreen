<div class="background">
  <div class="content">
    <slot />
  </div>
</div>

<style lang="scss">
  .background {
    --margin-w: 80px;
    --margin-h: 60px;

    background-color: var(--background);
    background-image: var(--background-gradient);

    display: flex;
    justify-content: center;
    align-items: center;

    position: relative;
    width: 100%;
    height: var(--screen-height, 100%);

    .content {
      position: absolute;
      width: calc(100% - var(--margin-w) * 2);
      height: calc(100% - var(--margin-h) * 2);

      background-color: var(--background);

      border-radius: 25px;
      box-shadow: 0 5px 25px 5px rgba(0, 0, 0, 0.2);
    }
  }
</style>
