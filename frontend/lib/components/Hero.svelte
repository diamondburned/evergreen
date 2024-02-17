<div class="background">
  <div class="content">
    <slot />
  </div>
</div>

<style lang="scss">
  .background {
    --margin-w: 80px;
    --margin-h: 60px;

    --size: 85%;
    --color-1: 149, 177, 176;
    --color-2: 138, 142, 174;
    --color-3: 155, 191, 101;

    background: radial-gradient(
        circle at calc(50%) calc(100%),
        rgba(var(--color-1), 1) 0%,
        rgba(var(--color-1), 0) var(--size)
      ),
      radial-gradient(
        circle at calc(0%) calc(0%),
        rgba(var(--color-2), 1) 0%,
        rgba(var(--color-2), 0) var(--size)
      ),
      radial-gradient(
        circle at calc(100%) calc(0%),
        rgba(var(--color-3), 1) 0%,
        rgba(var(--color-3), 0) var(--size)
      );

    display: flex;
    justify-content: center;
    align-items: center;

    position: relative;
    width: 100%;
    height: 100%;

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
