let signupModule = new Module({
  template: './templates/sign_up.html',
  model: {
    login: 'fiifi',
    password: 'fiifi'
  },
  handlers: {
    loginButton: function(model) {
      alert(model.login + ' ' + model.password)
      VHrequest({
        method: 'POST',
        url: SERVER + '/sign/in',
        data: {
          login: model.login,
          password: model.password
        }
      }).then((response) => {
        alert(response)
      })
    }
  }
})
