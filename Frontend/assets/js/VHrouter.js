function Router(routes) {

  this.nowActive = undefined
  this.container = undefined

  this.routes = new Map()
  for (let route of routes) {
    this.routes.set(route[0], route[1])
  }


  this.routerLogic = function() {

    let location = document.location.hash.replace('#', '')
    location = location != '' ? location : '/'

    if (this.nowActive != undefined) {
      this.nowActive.hide()
    }
    if (this.routes.has(location)) {
      this.nowActive = this.routes.get(location)
      this.nowActive.show(this.container)
    }
  }

  this.init = function(container) {
    this.container = container
    window.addEventListener('hashchange', () => { this.routerLogic() })
  }

}
