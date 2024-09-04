/* tslint:disable */
/* eslint-disable */
/**
 * portfolio API
 * Documentation of API endpoints of portfolio
 *
 * The version of the OpenAPI document: 1.0.0
 *
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { mapValues } from '../runtime';
/**
 *
 * @export
 * @interface User
 */
export interface User {
  /**
   *
   * @type {string}
   * @memberof User
   */
  name?: string;
  /**
   *
   * @type {string}
   * @memberof User
   */
  readonly url: string;
}

/**
 * Check if a given object implements the User interface.
 */
export function instanceOfUser(value: object): value is User {
  if (!('url' in value) || value['url'] === undefined) return false;
  return true;
}

export function UserFromJSON(json: any): User {
  return UserFromJSONTyped(json, false);
}

export function UserFromJSONTyped(
  json: any,
  ignoreDiscriminator: boolean,
): User {
  if (json == null) {
    return json;
  }
  return {
    name: json['name'] == null ? undefined : json['name'],
    url: json['url'],
  };
}

export function UserToJSON(value?: Omit<User, 'url'> | null): any {
  if (value == null) {
    return value;
  }
  return {
    name: value['name'],
  };
}
