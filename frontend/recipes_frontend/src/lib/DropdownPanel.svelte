<script>
    export let options = [];
    export let selected = [];
    export let toggleOption = () => {};
  </script>
  
  <div class="panel">
    {#each options as option}
      <label>
        <input
          type="checkbox"
          checked={selected.includes(option)}
          on:change={() => toggleOption(option)}
        />
        {option}
      </label>
    {/each}
  </div>
  
  <style>
    .panel {
      position: absolute;
      top: 100%; 
      left: 0;
      margin-top: 0.5rem;
      background: white;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
      padding: 1rem;
      border-radius: 16px;
      z-index: 1000;
      width: 190px;
    }
  
    :global(body.dark) .panel {
      background-color: #1e1e1e;
      color: #f5f5f5;
    }
  
    label {
      display: flex;
      align-items: center;
      gap: 0.6rem;
      font-size: 1rem;
      font-weight: 500;
      color: #222;
      margin-bottom: 0.6rem;
    }
  
    :global(body.dark) label {
      color: #f5f5f5;
    }
  
    input[type='checkbox'] {
      transform: scale(1.2);
      accent-color: #0077cc;
      cursor: pointer;
    }
  </style>
