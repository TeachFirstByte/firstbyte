<template>
  <div class="container">
    <div class="loaner-content">
      <div class="loaner-intro">
	<h1 class="font-weight-bold">Loaner Program</h1>
	<p>Borrow electronics from FirstByte for your classroom</p>
	
	<p>If you're in the Boston area and need materials, we're here to
	  help. FirstByte's loaner program gives local educators the chance
	  to borrow various technology kits to use in their clasrooms.</p>
      </div>
      <hr>
      <p class="font-weight-bold">Our Inventory</p>
      <p>Please note: you must be logged in to reserve our technology kits.</p>
      <kit />
    </div>
  </div>
</template>

<script>
export default {
}
</script>

<style scoped>
.loaner-content {
    width: 100%;
    height: 20em;
}
.loaner-intro {
    display: flex;
    width: 40%;
    flex-direction: column;
}

hr {
    margin: 1.5rem 0 auto;
}


</style>
