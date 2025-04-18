<script>
    import DropdownTrigger from '$lib/DropdownTrigger.svelte';
    import DropdownPanel from '$lib/DropdownPanel.svelte';
    import { browser } from '$app/environment';
    import { onMount, onDestroy } from 'svelte';
  
    $: {
    if (browser) {
      document.body.classList.toggle('dark', darkMode);
    }
    }
  
    let searchQuery = '';
    let searchResults = [];
  
    const dietaryOptions = [
      'Vegan', 'Vegetarian', 'Pescatarian', 'Gluten Free', 'Lactose Intolerant',
      'Nut Free', 'Dairy Free', 'Keto', 'Paleo', 'Halal', 'Kosher',
      'Low Carb', 'Low Fat', 'High Protein'    
    ];
  
    const cuisineOptions = [
      'American', 'Brazilian', 'British', 'Chinese', 'French', 'Greek',
      'Indian', 'Italian', 'Japanese', 'Korean', 'Mexican', 'Middle Eastern',
      'Spanish', 'Thai', 'Turkish', 'Vietnamese'
    ];
  
    let selectedDietary = [];
    let selectedCuisine = [];
  
    let showDietary = false;
    let showCuisine = false;
    let darkMode = false;
  
    function toggleOption(list, option) {
      return list.includes(option)
        ? list.filter(o => o !== option)
        : [...list, option];
    }
  
    async function handleSearch() {
      if (!browser || !searchQuery.trim()) return;
      
        const queryParams = new URLSearchParams();
        queryParams.set('q', searchQuery);
  
        selectedDietary.forEach(diet => queryParams.append('diet', diet));

        selectedCuisine.forEach(cuisine => queryParams.append('cuisine', cuisine));

      try {
        const response = await fetch(`http://127.0.0.1:5000/search?q=${queryParams.toString()}`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const data = await response.json();
        searchResults = data.results;
      } catch (error) {
        console.error('Search failed:', error);
      }
    }
  
    function closeAllPanels(except = null) {
      showDietary = except === 'dietary';
      showCuisine = except === 'cuisine';
    }
  
    function handleClickOutside(event) {
      const dropdowns = document.querySelectorAll('.dropdown-wrapper');
      const clickedInside = Array.from(dropdowns).some(dropdown => dropdown.contains(event.target));
      if (!clickedInside) closeAllPanels();
    }
  
    function removeFilter(type, value) {
      if (type === 'dietary') selectedDietary = selectedDietary.filter(item => item !== value);
      if (type === 'cuisine') selectedCuisine = selectedCuisine.filter(item => item !== value);
    }
  
    function clearAllFilters() {
    selectedDietary = [];
    selectedCuisine = [];
    }
  
    function resetHome() {
    searchQuery = '';
    searchResults = [];
    showSaved = false;
    }
  
    onMount(() => {
      if (browser) window.addEventListener('click', handleClickOutside);
    });
  
    onDestroy(() => {
      if (browser) window.removeEventListener('click', handleClickOutside);
    });
  </script>
  
  <h1 class="title">
    <span class="logo">🍲</span>
    <span class="clickable-title" on:click={resetHome}>Recipe Search Engine</span>
    <label class="toggle-switch">
      <input type="checkbox" bind:checked={darkMode}>
      <span class="slider"></span>
    </label>
  </h1>
  
  <div class="search-container">
    <input 
      type="text" 
      placeholder="What would you like to cook?" 
      bind:value={searchQuery}
      on:keydown={(e) => e.key === 'Enter' && handleSearch()} 
    />
    <button class="search-button" on:click={handleSearch}>🔍</button>
  </div>
  
  <div class="filter-wrapper">
    <div class="filter-row">
      <div class="dropdown-wrapper">
        <DropdownTrigger label="Dietary Requirements" on:click={() => closeAllPanels('dietary')} />
        {#if showDietary}
          <DropdownPanel options={dietaryOptions} selected={selectedDietary} toggleOption={(opt) => selectedDietary = toggleOption(selectedDietary, opt)} />
        {/if}
      </div>
  
      <div class="dropdown-wrapper">
        <DropdownTrigger label="Cuisine" on:click={() => closeAllPanels('cuisine')} />
        {#if showCuisine}
          <DropdownPanel options={cuisineOptions} selected={selectedCuisine} toggleOption={(opt) => selectedCuisine = toggleOption(selectedCuisine, opt)} />
        {/if}
      </div>
    </div>
  
      {#if selectedDietary.length > 0 || selectedCuisine.length > 0}
      <div class="active-filters">
        {#each selectedDietary as diet}
          <span class="filter-tag">{diet} <button on:click={() => removeFilter('dietary', diet)}>×</button></span>
        {/each}
        {#each selectedCuisine as cuisine}
          <span class="filter-tag">{cuisine} <button on:click={() => removeFilter('cuisine', cuisine)}>×</button></span>
        {/each}
        <button class="clear-all" on:click={clearAllFilters}>Reset Filters</button>
      </div>
    {/if}
  </div>
  
  
  {#if searchResults.length > 0}
    <div class="results">
      <h2>Results:</h2>
      {#each searchResults as result}
        <div class="recipe-card">
          <h3>{result.columns.name.text}</h3>
          <p><strong>Ingredients:</strong> {result.columns.ingredients.text.replace(/ /g, ', ')}</p>
          <p><strong>Steps:</strong> {result.columns.steps.text.replace(/,/g, ' → ')}</p>
          <p><strong>Description:</strong> {result.columns.description.text}</p>
          <div class="card-actions">
          </div>
        </div>
      {/each}
    </div>
  {/if}  
  
  <footer class="footer">
    Bon Appétit! 👩‍🍳
  </footer>
  
  
  <style>
    :global(body) {
      font-family: 'Inter', 'Georgia', serif;
      background-color: var(--bg);
      color: var(--text);
      transition: all 0.3s ease;
    }
  
    :global(:root) {
    --bg: #f9f9f9;           
    --text: #1a1a1a;         
    --surface: #ffffff;     
    --accent: #e74c3c;      
    }
  
    :global(body.dark) {
    --bg: #1e1e1e;           
    --text: #e0e0e0;        
    --surface: #2c2c2c;     
    --accent: #f26d6d;     
    }
  
  
    .title {
      text-align: center;
      font-size: 2.5rem;
      margin-top: 1rem;
      font-weight: 700;
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 1rem;
    }
  
    .logo {
      font-size: 2rem;
    }
  
    .toggle-switch {
      position: absolute;
      right: 2rem;
      top: 1.5rem;
    }
  
    .toggle-switch input {
      display: none;
    }
  
    .slider {
      width: 40px;
      height: 20px;
      background: #ccc;
      border-radius: 20px;
      position: relative;
      display: inline-block;
      cursor: pointer;
    }
  
    .slider::before {
      content: "";
      position: absolute;
      width: 16px;
      height: 16px;
      background: white;
      border-radius: 50%;
      top: 2px;
      left: 2px;
      transition: transform 0.3s ease;
    }
  
    input:checked + .slider::before {
      transform: translateX(20px);
    }
  
    input:checked + .slider {
      background: #4caf50;
    }
  
    .search-container {
      display: flex;
      align-items: center;
      border: 1px solid #ccc;
      border-radius: 20px;
      padding: 0.4rem 1rem;
      width: fit-content;
      margin: 2rem auto;
    }
  
    input[type="text"] {
    background: transparent;
    border: none;
    outline: none;
    font-size: 1rem;
    padding: 0.4rem 0.6rem;
    width: 280px;
    color: var(--text); /* 👈 EKLENDİ */
    }
  
  
    .search-button {
      background: none;
      border: none;
      font-size: 1.6rem;
      cursor: pointer;
      padding-left: 0.3rem;
      transition: transform 0.15s ease;
    }
  
    .search-button:hover {
      transform: scale(1.2);
      font-size: 1.8rem
    }
  
    .filter-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    margin-top: 1rem;
    }
  
    .filter-row {
      display: flex;
      justify-content: center;
      flex-wrap: wrap;
      gap: 2rem;
    }
  
    .active-filters {
      display: flex;
      justify-content: center;
      flex-wrap: wrap;
      gap: 1rem;
    }
  
    .dropdown-wrapper {
    position: relative;
    }
  
    .filter-tag {
    display: flex;
    align-items: center;
    background-color: #eee;
    padding: 0.3rem 0.7rem;
    border-radius: 999px;
    font-size: 0.9rem;
    font-weight: 500;
    color: #000;
    transition: background 0.3s, color 0.3s;
    }
  
    body.dark .filter-tag {
      background-color: #333;
      color: #f5f5f5;
    }
  
    .filter-tag button {
      margin-left: 0.5rem;
      border: none;
      background: none;
      cursor: pointer;
      font-weight: bold;
      color: inherit;
    }
  
    .clear-button {
    background-color: #e74c3c;
    color: white;
    border: none;
    border-radius: 999px;
    padding: 0.4rem 1rem;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.2s ease;
    }
  
    .clear-button:hover {
      background-color: #c0392b;
    }
  
  
    body.dark .clear-all {
      border-color: #555;
      color: #f5f5f5;
    }
  
    body.dark .clear-all:hover {
      background-color: #ff5a5a;
      color: white;
    }
  
  
    .results {
      margin: 3rem auto;
      max-width: 800px;
      padding: 0 1rem;
    }
  
    .recipe-card {
    background: var(--surface);
    color: var(--text);
    border: 1px solid #444;
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 1.5rem;
    transition: background 0.3s ease, color 0.3s ease;
    }
  
    .recipe-card h3 {
      margin: 0;
      font-size: 1.2rem;
      color: var(--accent);
    }
  
    .recipe-card p {
      margin: 0.3rem 0;
    }
    .recipe-card:hover {
      transform: scale(1.01);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
  
    .footer {
    text-align: center;
    margin-top: 4rem;
    font-size: 2rem;
    font-family: 'Caveat', cursive;
    color: var(--text);
    opacity: 0.85;
    padding-bottom: 2.5rem;
    margin-bottom: 2rem;
    }
    
    .clickable-title {
    cursor: pointer;
    transition: opacity 0.2s ease;
    }
    .clickable-title:hover {
      opacity: 0.7;
    }
  
    .footer span {
    vertical-align: middle; 
    }
  
    .footer {
    animation: fadeIn 1.5s ease-in;
    }
  
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
    }
  
  
  
</style>
