#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/7/18 10:07
# @Author  : weibing.ma@daocloud.io
# @FileName: jfrog_post_api.py

from flask import Flask, request
import docker

client = docker.DockerClient(base_url='tcp://10.6.203.60:2375')
app = Flask(__name__)


@app.route("/push_image", methods=['POST'])
def push_images():
    """判断请求类型是否是 post，并将请求 body 存储在 post_request_info,并判断其是否为字典"""
    if request.method == 'POST':
        if not request.form:
            return 'POST 请求表单为空'
        post_request_info = request.form
        if isinstance(post_request_info, dict):
            jfrog_image = post_request_info.get('jfrog_image')
            jfrog_registry_url = post_request_info.get('jfrog_registry_url')
            prod_registry_url = post_request_info.get('prod_registry_url')
            cuser = post_request_info.get('caas_user')
            cpasswd = post_request_info.get('caas_passwd')
            juser = post_request_info.get('jfrog_user')
            jpasswd = post_request_info.get('jfrog_passwd')
            try:
                client.login(username='{u}'.format(u=juser), password='{p}'.format(p=jpasswd),
                             registry='{jurl}'.format(jurl=jfrog_registry_url))
                try:
                    client.images.pull('{img}'.format(img=jfrog_image))
                    jfrogimagetag = '{img}'.format(img=jfrog_image)
                    prodimagetag = '{url}/'.format(url=prod_registry_url) + '{img}'.format(img=jfrog_image)
                    client.api.tag('{j_tag}'.format(j_tag=jfrogimagetag), '{p_tag}'.format(p_tag=prodimagetag))
                    try:
                        client.login(username='{u}'.format(u=cuser), password='{p}'.format(p=cpasswd),
                                     registry='{curl}'.format(curl=prod_registry_url))
                        if client.api.push('{p_tag}'.format(p_tag=prodimagetag)):
                            return {'Response': 200, 'Info': 'PushFinished'}
                        else:
                            return {'Response': 404, 'Info': 'PushFailed'}
                    except Exception as dlogin_err:
                        return {'Response': 500, 'Info': 'DceLoginFailed',
                                'Result': dlogin_err.__dict__.get('explanation')}
                except Exception as img_err:
                    return {'Response': 404, 'Info': 'ImageNotFound',
                            'Result': img_err.__dict__.get('explanation')}
            except Exception as jlogin_err:
                return {'Response': 500, 'Info': 'JfrogLoginFailed',
                        'Result': jlogin_err.__dict__.get('explanation')}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3002)
