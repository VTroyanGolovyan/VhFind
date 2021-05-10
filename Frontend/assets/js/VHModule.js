function Module(settings) {
  this.templateText = ''
  this.create = function() {
    if (settings.template) {
      this.template
    }
  }

  this.show = function(container) {
    if (this.templateText == '') {
      VHrequest({
        method: 'GET',
        url: settings.template
      }).then((data) => {
        this.templateText = data
        this.show(container)
      })
    } else {
      container.innerHTML = this.templateText
    }
  }

  this.hide = function() {

  }

}
