import request from '@/utils/request'

export function login(data) {
  console.log(data)
  return request({
    url: '/login',
    method: 'post',
    data
  })
}

export function getUsers(query) {
  return request({
    url: '/user/list',
    method: 'get',
    params: query
  })
}

export function addUser(data) {
  return request({
    url: '/user/add',
    method: 'post',
    data
  })
}

export function delUser(data) {
  return request({
    url: '/user/del',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/user/info',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/logout',
    method: 'post'
  })
}
