import request from '@/utils/request'

export function getProductServer(query) {
  return request({
    url: '/product/server',
    method: 'get',
    params: query
  })
}
