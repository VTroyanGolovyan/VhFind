function updateWatching(map, model) {
  map.forEach((containers, key, map) => {
    for (let container of containers) {
      if (container.tagName.toLowerCase() == 'input') {
        container.value = model[key]
      } else {
        container.innerHTML = model[key]
      }
    }
  });
}

function Module(settings) {

  this.templateText = ''
  this.create = function() {
    if (settings.template) {
      this.template
    }
  }

  this.modelProxy = {}

  let nowWatching = new Map()
  for (let property in settings.model) {
    let proxy = this.modelProxy
    Object.defineProperty(
      this.modelProxy,
      property,
      {
        set: function (x) {
          settings.model[property] = x
          updateWatching(nowWatching, proxy)
        },
        get: function() {
          return settings.model[property]
        }
      }
    );
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
      this.bind(container)
    }
  }

  this.bind = function(container) {
    let children = container.childNodes;
    try {
      if (container.getAttribute('vh-model')) {
        let inModel = container.getAttribute('vh-model')
        if (nowWatching.has(inModel)) {
          nowWatching.get(inModel).push(container)
        } else {
          nowWatching.set(inModel, [container])
        }
        if (container.tagName.toLowerCase() == 'input') {
          container.value = eval('settings.model.' + inModel)
          container.oninput = () => {
            eval('this.modelProxy.' + inModel +' = "' + container.value + '"')
          }
        } else {
          container.innerHTML = eval('settings.model.' + inModel)
        }
      }
      if (container.getAttribute('vh-handler')) {
        let handlername = container.getAttribute('vh-handler')
        container.onclick = () => {
          eval('settings.handlers.' + handlername + '(this.modelProxy)')
        }
      }
    } catch(ignore) {}


    for (var i = 0; i < children.length; ++i) {
      this.bind(children[i])
    }

  }

  this.hide = function() {
    nowWatching.clear()
  }

}
