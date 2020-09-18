import request from '@/utils/request'

export function getProjects(query) {
  return request({
    url: '/project/list',
    method: 'get',
    params: query
  })
}

export function addProject(data) {
  return request({
    url: '/project/upsert',
    method: 'post',
    data
  })
}

export function delProject(data) {
  return request({
    url: '/project/del',
    method: 'post',
    data
  })
}
