<script>
    import { createEventDispatcher } from 'svelte';
    export let label = '';
    const dispatch = createEventDispatcher();
  
    function handleClick() {
      dispatch('click');
    }
  </script>
  
  <button class="trigger-box" on:click={handleClick}>
    {label}
  </button>
  
  <style>
    .trigger-box {
      background: rgb(237, 237, 237);
      border: none;
      border-radius: 16px;
      padding: 1rem 1.5rem;
      font-weight: 600;
      font-size: 1rem;
      cursor: pointer;
      transition: all 0.3s ease;
      min-width: 220px;
      box-shadow: 0 6px 12px rgba(0, 0, 0, 0.06);
    }
  
    .trigger-box:hover {
      background-color: rgb(227, 227, 227);
      transform: translateY(-1px);
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
    }
  
    .trigger-box:focus {
      outline: none;
      box-shadow: 0 0 0 2px rgba(0, 119, 204, 0.25);
    }
  </style>
