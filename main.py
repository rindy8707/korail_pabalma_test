
# connectivity_mcp_server.py
import socket
import subprocess

import requests
import httpx
#from mcp.server.fastmcp import FastMCP
import urllib
#mcp = FastMCP(host="0.0.0.0", port="8080")
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("korail_telnet")


@mcp.tool()
def check_service(timeout_seconds: int = 180) -> dict:
    """
    고객사 목적지로 telnet 요청을 보내 응답을 확인합니다.
    """

    ip = "175.123.132.5"
    port = 7777  # 정수로
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)  # 5초 타임아웃
    
    try:
        result = sock.connect_ex((ip, port))
        if result == 0:
            return {
                "success": True,
                "message": f"연결 성공: {ip}:{port}",
                "errno": 0
            }
        else:
            return {
                "success": False,
                "message": f"연결 실패 (errno: {result})",
                "errno": result
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"예외 발생: {str(e)}",
            "errno": None
        }
    finally:
        sock.close()

# @mcp.tool()
# def get_json(
#     url: str,
#     headers: dict = None,
#     params: dict = None,
#     timeout: int = 10,
# ) -> dict:
#     """
#     GET 요청을 보내고 JSON 응답을 받아옵니다. (Content-Type: application/json)

#     Args:
#         url: 요청할 URL (예: https://api.example.com/v1/users)
#         headers: 추가 헤더 (예: {"Authorization": "Bearer xxx"})
#         params: 쿼리 파라미터 (예: {"page": 1, "size": 10})
#         timeout: 타임아웃(초)
#     """
#     default_headers = {
#         "Accept": "application/json",
#         "Content-Type": "application/json",
#     }
#     if headers:
#         default_headers.update(headers)

#     try:
#         response = requests.get(
#             url,
#             headers=default_headers,
#             params=params,
#             timeout=timeout,
#         )

#         # 응답 바디 파싱 시도 (JSON이 아닐 수도 있으므로 안전하게 처리)
#         try:
#             body = response.json()
#         except ValueError:
#             body = response.text

#         return {
#             "success": response.ok,  # 200~399면 True
#             "http_status": response.status_code,
#             "url": response.url,
#             "elapsed_ms": round(response.elapsed.total_seconds() * 1000, 1),
#             "data": body,
#         }

#     except requests.exceptions.SSLError as e:
#         return {
#             "success": False,
#             "error_type": "SSLError",
#             "message": f"SSL 인증서 오류: {e}",
#         }
#     except requests.exceptions.ConnectTimeout:
#         return {
#             "success": False,
#             "error_type": "ConnectTimeout",
#             "message": f"연결 타임아웃 ({timeout}초)",
#         }
#     except requests.exceptions.ConnectionError as e:
#         return {
#             "success": False,
#             "error_type": "ConnectionError",
#             "message": f"연결 실패 (Connection reset, refused 등): {e}",
#         }
#     except requests.exceptions.Timeout:
#         return {
#             "success": False,
#             "error_type": "Timeout",
#             "message": f"응답 타임아웃 ({timeout}초)",
#         }
#     except requests.exceptions.RequestException as e:
#         return {
#             "success": False,
#             "error_type": "RequestException",
#             "message": f"요청 오류: {e}",
#         }
@mcp.tool()
def check_http(
    url: str,
    timeout_seconds: int = 10,
) -> dict:
    """
    기상특보목록을 조회하도록 합니다.
    url 예: http://DOMAIN:PORT/API_PATH
    """
    headers = {
        "Accept": "application/json",
        "User-Agent": "curl/8.0",
        # "Authorization": "Bearer ...",
    }
    response = requests.get(url, headers=headers, timeout=timeout_seconds, verify=False)

    return {
        "ok": True,
        "url": url,
        "status_code": response.status_code,
        "headers": dict(response.headers),
        "body_preview": response.text[:500],
    }


# @mcp.tool()
# def check_url(url: str, timeout: int = 5, method: str = "GET") -> dict:
#     """
#     URL 접속 가능 여부와 상태를 확인합니다.

#     Args:
#         url: 확인할 URL (예: https://example.com)
#         timeout: 타임아웃(초)
#         method: HTTP 메서드 (GET 또는 HEAD, 기본값 GET)
#     """
#     try:
#         response = requests.request(
#             method.upper(),
#             url,
#             timeout=timeout,
#             allow_redirects=True,
#         )
#         return {
#             "success": response.ok,  # 200~399면 True
#             "url": url,
#             "final_url": response.url,  # 리다이렉트 최종 목적지
#             "http_status": response.status_code,
#             "elapsed_ms": round(response.elapsed.total_seconds() * 1000, 1),
#             "message": f"응답 코드: {response.status_code}",
#         }

#     except requests.exceptions.SSLError as e:
#         return {"success": False, "url": url, "message": f"SSL 인증서 오류: {e}"}
#     except requests.exceptions.ConnectTimeout:
#         return {"success": False, "url": url, "message": f"연결 타임아웃 ({timeout}초)"}
#     except requests.exceptions.ConnectionError as e:
#         return {"success": False, "url": url, "message": f"연결 실패: {e}"}
#     except requests.exceptions.Timeout:
#         return {"success": False, "url": url, "message": f"응답 타임아웃 ({timeout}초)"}
#     except requests.exceptions.RequestException as e:
#         return {"success": False, "url": url, "message": f"요청 오류: {e}"}

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8080)
