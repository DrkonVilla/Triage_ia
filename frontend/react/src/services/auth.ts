import { jwtDecode } from 'jwt-decode';

interface DecodedToken {
  sub: string;
  exp?: number | string;
}

export const isAuthenticated = (): boolean => {
  const token = localStorage.getItem('access_token');
  if (!token) return false;
  
  try {
    const decoded = jwtDecode<DecodedToken>(token);
    if (decoded.exp === undefined || decoded.exp === null) {
      // Algunos emisores no incluyen exp; en ese caso, asumimos válido si el token existe
      return true;
    }

    const expSeconds = typeof decoded.exp === 'string' ? Number(decoded.exp) : decoded.exp;
    if (!Number.isFinite(expSeconds)) {
      return true;
    }

    const currentTimeSeconds = Date.now() / 1000;
    return expSeconds > currentTimeSeconds;
  } catch {
    return false;
  }
};

export const getUserRole = (): string | null => {
  const userStr = localStorage.getItem('user');
  if (!userStr) return null;
  try {
    const user = JSON.parse(userStr);
    return user.rol;
  } catch {
    return null;
  }
};

export const getUserName = (): string | null => {
  const userStr = localStorage.getItem('user');
  if (!userStr) return null;
  try {
    const user = JSON.parse(userStr);
    return `${user.nombres} ${user.apellidos}`;
  } catch {
    return null;
  }
};