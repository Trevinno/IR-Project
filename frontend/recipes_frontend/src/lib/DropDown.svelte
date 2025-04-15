<script>
    import DropdownTrigger from './DropdownTrigger.svelte';
    import DropdownPanel from './DropdownPanel.svelte';
    export let label = '';
    export let options = [];
    export let selected = [];
  
    let isOpen = false;
  
    function toggleDropdown() {
      isOpen = !isOpen;
    }
  
    function toggleOption(option) {
      if (selected.includes(option)) {
        selected = selected.filter(o => o !== option);
      } else {
        selected = [...selected, option];
      }
    }
  </script>
  
  <div class="dropdown-wrapper">
    <DropdownTrigger {label} {isOpen} on:click={toggleDropdown} />
  
    {#if isOpen}
      <DropdownPanel>
        {#each options as option}
          <label class="option">
            <input
              type="checkbox"
              checked={selected.includes(option)}
              on:change={() => toggleOption(option)}
            />
            {option}
          </label>
        {/each}
      </DropdownPanel>
    {/if}
  </div>
  
  <style>
    .dropdown-wrapper {
      position: relative;
      width: 250px;
      max-width: 100%;
    }
  
    .option {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 0.95rem;
      margin-bottom: 0.4rem;
    }
  
    input[type='checkbox'] {
      transform: scale(1.1);
      cursor: pointer;
    }
  
    input[type='checkbox']:hover {
      accent-color: #0077cc;
    }
  </style>
