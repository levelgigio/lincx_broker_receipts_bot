(async function loop() {
await (async function loop1() {
        
    await new Promise(function(resolve, reject) {
        setTimeout(() => {
            resolve(console.log('porra'))
        }, 1000)  
      });
    
      await new Promise(function(resolve, reject) {
        setTimeout(() => {
            resolve(console.log('buceta'))
        }, 500)  
      });
      return new Promise(function(resolve, reject) {
            resolve(1)
        })
      
    }
    )();
    console.log('krl')
})()

